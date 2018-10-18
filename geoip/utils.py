"""Utility functions relating to IP lookups."""

from collections import namedtuple

import ipaddress
from geoip2 import database, errors


class GeoIP():
    """GeoIP database.

    This class leverages the maxmind IP database.

    The free versions can be located here:

    https://dev.maxmind.com/geoip/geoip2/geolite2/
    """

    def __init__(self):
        """Initialize an unloaded GeoIP database."""
        self._initialized = False
        self._geo_asn = False
        self._geo_country = False
        self._geo_city = False

    def init_app(self, app):
        """Initialize the GeoIP instance from an application.

        :param app: application
        :type app: sanic.Sanic
        """
        self._geo_asn = database.Reader(app.config.get('MAXMIND_ASN_PATH'))
        self._geo_city = database.Reader(app.config.get('MAXMIND_CITY_PATH'))
        self._geo_country = database.Reader(
            app.config.get('MAXMIND_COUNTRY_PATH'))

        self._initialized = False

    def get_city(self, ip):
        """Get the city an IP is associated with."""
        return self._geo_city.city(ip).city.name

    def get_continent(self, ip):
        """Get the continent that an IP is associated with."""
        return self._geo_city.city(ip).continent.name

    def get_country(self, ip):
        """Get the country that an IP is associated with."""
        return self._geo_country.country(ip).country.name

    def get_asn_name(self, ip):
        """Get the ASN name of a specific IP."""
        return self._geo_asn.asn(ip).autonomous_system_organization

    def get_asn_num(self, ip):
        """Get the ASN number for the ASN of a specific IP."""
        return self._geo_asn.asn(ip).autonomous_system_number

    def get_location(self, ip):
        """Get the latitude and longitute of a specific IP."""
        return dict(
            lat=self._geo_city.city(ip).location.latitude,
            lon=self._geo_city.city(ip).location.longitude,
        )


def is_private(ip):
    """Determine if an IP is private."""
    return ipaddress.ip_address(ip).is_private


def is_public(ip):
    """Determine if an IP is public."""
    return ipaddress.ip_address(ip).is_global


def is_multicast(ip):
    """Determine if an IP is multicast."""
    return ipaddress.ip_address(ip).is_multicast


def is_reserved(ip):
    """Determine if an IP is in a reserved space."""
    return ipaddress.ip_address(ip).is_reserved


def is_unspecified(ip):
    """Determine if an IP is unspecified."""
    return ipaddress.ip_address(ip).is_unspecified


def get_ip_version(ip):
    """Determine the version of an IP."""
    return ipaddress.ip_address(ip).version


def is_ip(ip):
    """Determine if the IP is, indeed, an IP."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
