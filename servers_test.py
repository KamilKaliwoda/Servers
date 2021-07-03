#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from collections import Counter

from servers import ListServer, Product, Client, MapServer

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 1), Product('PP236', 3), Product('PP235', 2)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[1], products[3], products[2]]), Counter(entries))

    def test_get_entries_returns_sorted_entries(self):
        products = [Product('P12', 1), Product('PP234', 1), Product('PP236', 3), Product('PP235', 2)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertListEqual([products[1], products[3], products[2]], entries)

    def test_get_entries_returns_sorted_entries_over_max_entries(self):
        with self.assertRaises(Exception):
            products = [Product('PP234', 1), Product('PP236', 3), Product('PP235', 2), Product('PP275', 2), Product('PP265', 2), Product('PP255', 2)]
            for server_type in server_types:
                server = server_type(products)
                entries = server.get_entries(2)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_normal_execution2(self):
        products = [Product('PP234', 2), Product('PP235', 3), Product('PE236', 6)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(11, client.get_total_price(2))

    def test_total_price_for_normal_execution3(self):
        products = [Product('PP234', 2), Product('PPP235', 3), Product('PE236', 6)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(8, client.get_total_price(2))

    def test_total_price_error(self):
        products = [Product('PP234', 2), Product('PPP235', 3), Product('PE236', 6)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertIsNone(None, client.get_total_price(4))


if __name__ == '__main__':
    unittest.main()
