import unittest

from unittest import mock

from geoip.app import create_app


class BaseTestCase(unittest.TestCase):
    def setUp(self, *_):
        self.app = create_app()
