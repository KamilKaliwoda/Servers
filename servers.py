#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from typing import Optional, List, TypeVar
from abc import ABC, abstractmethod
from re import fullmatch
from copy import deepcopy


class Server(ABC):
    n_max_returned_entries: int = 5

    @abstractmethod
    def get_entries(self, n_letters: int = 1):
        raise NotImplementedError


class Product:
    # The class has an initialization method accepting arguments expressing the product name (str type) and its price (float type).
    def __init__(self, name, price):
        if not fullmatch(r"([a-z]|[A-Z])(.*\d)", name):
            raise ValueError
        self.name = name
        self.price = price

    def __eq__(self, other):
        return (self.name == other.name) and (self.price == other.price)

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Represents an exception related to finding too many products.
    def __init__(self, amount):
        super().__init__(f"To many fitting products! {amount} products found.")
 
# Each of the following server classes has:
#   (1) initialization method that takes a list of objects of type `Product` and sets the `products` attribute according to the type of product representation on the given server,
#   (2) the ability to invoke a class attribute `n_max_returned_entries` (type int) expressing the maximum allowed number of search results,
#   (3) the ability to invoke the `get_entries(self, n_letters)` method returning a list of products matching the search criterion.


class ListServer(Server):
    def __init__(self, products: List[Product]):
        self.products = deepcopy(products)

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        list_of_products: List[Product] = []
        pattern = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$'
        for p in self.products:
            if fullmatch(pattern, p.name):
                list_of_products.append(p)
        if len(list_of_products) > self.n_max_returned_entries:
            raise TooManyProductsFoundError(len(list_of_products))
        else:
            if list_of_products:
                list_of_products.sort(key=lambda product: product.price)
            return list_of_products


class MapServer(Server):
    def __init__(self, products: List[Product]):
        dct = {}
        for p in deepcopy(products):
            dct.setdefault(p.name, p)
        self.products = dct

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        pattern = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$'
        list_of_products: List[Product] = []
        for keys in self.products.keys():
            if fullmatch(pattern, keys):
                list_of_products.append(self.products[keys])
        if len(list_of_products) > self.n_max_returned_entries:
            raise TooManyProductsFoundError(len(list_of_products))
        else:
            if list_of_products:
                list_of_products.sort(key=lambda product: product.price)
            return list_of_products


server_type = TypeVar('server_type', bound=Server)


class Client:
    # Class has an initialization method that accepts an object representing the server.
    def __init__(self, server: server_type):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            sorted_lst = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None

        if sorted_lst:
            return sum([p.price for p in sorted_lst])
        else:
            return None

