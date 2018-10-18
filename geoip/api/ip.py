"""API blueprint relating to IP resources."""

from aiocache.serializers import JsonSerializer

from sanic import Blueprint
from sanic.exceptions import InvalidUsage
from sanic.response import json

from geoip.utils import is_public, is_ip
from geoip.extensions import ip_lookup

blueprint = Blueprint('geoip_api')


def get_profile(ip):
    """Create a dictionary detailing a variety of information about an IP."""
    if not is_ip(ip):
        raise InvalidUsage(f'{ip} is not a valid ip')
    if is_public(ip):
        asn_num = ip_lookup.get_asn_num(ip)
        asn = ip_lookup.get_asn_name(ip)
        return dict(
            ip=ip,
            city=ip_lookup.get_city(ip),
            country=ip_lookup.get_country(ip),
            continent=ip_lookup.get_continent(ip),
            locatio=ip_lookup.get_location(ip),
            # This likely should be split to seperate
            #  ASN & ASN_NUM make it easy on consumers.
            org=f'{asn_num} {asn}',
        )
    return dict(ip=ip, bogon=True)


@blueprint.route("/")
async def index(request):
    """Return the profile of the remote IP that made the request."""
    remote_addr = request.ip
    profile = get_profile(remote_addr)
    return(json(profile))


@blueprint.route("/<ip>")
async def geo_ip(request, ip):
    """Given an IP, return information about the IP."""
    if not is_ip(ip):
        raise InvalidUsage(f'{ip} is not a valid ip')
    profile = get_profile(ip)
    return json(profile)


@blueprint.route("/bulk", methods=["POST"])
async def bulk_geo_ip(request):
    """Given a JSON list of IPs, return the profile of each IP."""
    ip_list = request.json
    if not isinstance(ip_list, list):
        raise InvalidUsage('This endpoint only supports a list.')
    results = [get_profile(ip) for ip in ip_list]
    return json(dict(results=results))


@blueprint.route("/<ip>/<field>")
async def return_ip_profile(request, ip, field):
    """Return a specific field of an IP's profile."""
    profile = get_profile(ip)
    if field not in profile:
        raise InvalidUsage(f'{field} does not exist in the profile fields.')
    # This doesn't feel very API like. Returning a string!?
    return json(profile.get(field))
