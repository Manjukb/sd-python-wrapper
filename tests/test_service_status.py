#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mock import patch
from serverdensity.api import ApiClient
from serverdensity.api import ServiceStatus


class ServiceStatusTest(unittest.TestCase):

    @patch.object(ApiClient, '_make_request')
    def setUp(self, mock_make_request):
        self.client = ApiClient('aeou')
        self.client._make_request = mock_make_request
        self.client._make_request.return_value = {'service_status': 'result'}
        self.service_status = ServiceStatus(api=self.client)

    def test_service_status_overall(self):
        self.service_status.overall(1)
        self.client._make_request.assert_called_with(
            data=None,
            method='GET',
            url=ServiceStatus.PATHS['overall'].format(1),
            params=None
        )

    def test_service_status_location(self):
        self.service_status.location(1)
        self.client._make_request.assert_called_with(
            data=None,
            method='GET',
            url=ServiceStatus.PATHS['location'].format(1),
            params=None
        )

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())