#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from serverdensity import Response


class ResponseTest(unittest.TestCase):

    def setUp(self):
        self.data = {
            'property': 'result',
            'data': {'some_more': 'result'}
        }

    def tearDown(self):
        pass

    def test_a_single_property_works(self):
        response = Response(self.data)
        self.assertEqual(response.property, 'result')

    def test_a_deep_property_works(self):
        response = Response(self.data)
        self.assertEqual(response.data.some_more, 'result')

    @unittest.skip('not implemented')
    def test_response_cant_have_property_with_existing_method(self):
        self.data['_existing_method'] = 'test'
        with self.assertRaises(ValueError):
            response = Response(self.data

    def test_response_contains_a_list_of_response_objects(self):
        data = {'data': [{'1': 'a'}, {'2': 'b'}]}
        response = Response(data)
        self.assertEqual(isinstance(response.data[0], Response), True)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())