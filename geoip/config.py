"""Configuration for GeoIP application."""

import os


class DefaultConfig:
    """Default configuration for geoip application."""

    MAXMIND_CITY_PATH = '/usr/local/share/GeoIP/GeoLite2-City.mmdb'
    MAXMIND_COUNTRY_PATH = '/usr/local/share/GeoIP/GeoLite2-Country.mmdb'
    MAXMIND_ASN_PATH = '/usr/local/share/GeoIP/GeoLite2-ASN.mmdb'


class DevConfig:
    """Dev Configuration for geoip application."""

    MAXMIND_CITY_PATH = os.path.expanduser(
        '~/.maxmind-data/GeoLite2-City.mmdb')
    MAXMIND_COUNTRY_PATH = os.path.expanduser(
        '~/.maxmind-data/GeoLite2-Country.mmdb')
    MAXMIND_ASN_PATH = os.path.expanduser('~/.maxmind-data/GeoLite2-ASN.mmdb')
    DEBUG = True
