import unittest

from unittest import mock

from geoip.app import create_app

class TestApplicationConfigurable(unittest.TestCase):
    """Test that the application factory is configurable."""
    @mock.patch('geoip.utils.GeoIP.init_app')
    def test_config_value_follows(self, _):
        class FooConfig:
            TEST = True
        app = create_app(config=FooConfig)
        self.assertEqual(app.config.TEST, True)
