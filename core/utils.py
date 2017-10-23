from geoip2 import database, errors
import ipaddress

geo_city = database.Reader("/usr/local/share/GeoIP/GeoLite2-City.mmdb")
geo_country = database.Reader("/usr/local/share/GeoIP/GeoLite2-Country.mmdb")
geo_asn = database.Reader("/usr/local/share/GeoIP/GeoLite2-ASN.mmdb")

def get_city(ip):
    return(geo_city.city(ip).city.name)

def get_continent(ip):
    return(geo_city.city(ip).continent.name)

def get_country(ip):
    return(geo_country.country(ip).country.name)

def get_asn_name(ip):
    return(geo_asn.asn(ip).autonomous_system_organization)

def get_asn_num(ip):
    return(geo_asn.asn(ip).autonomous_system_number)

def get_location(ip):
    return( { "lat" : geo_city.city(ip).location.latitude, "lon" : geo_city.city(ip).location.longitude } )

def is_private(ip):
    return(ipaddress.ip_address(ip).is_private)

def is_public(ip):
    return(ipaddress.ip_address(ip).is_global)

def is_multicast(ip):
    return(ipaddress.ip_address(ip).is_multicast)

def is_reserved(ip):
    return(ipaddress.ip_address(ip).is_reserved)

def is_unspecified(ip):
    return(ipaddress.ip_address(ip).is_unspecified)

def get_ip_version(ip):
    return(ipaddress.ip_address(ip).version)

def get_profile(ip):
    try:
        if is_public(ip):
            return({
                "ip" : ip,
                "city" : get_city(ip),
                "country" : get_country(ip),
                "continent" : get_continent(ip),
                "location" : get_location(ip),
                "org" : "%s %s" % (get_asn_num(ip), get_asn_name(ip))
            })
        elif is_private(ip):
            return ({
                "ip" : ip,
                "bogon" : True
            })
        elif is_multicast(ip):
            return ({
                "ip" : ip,
                "bogon" : True
            })
        elif is_reserved(ip):
            return ({
                "ip" : ip,
                "bogon" : True
            })
        elif is_unspecified(ip):
            return ({
                "ip" : ip,
                "bogon" : True
            })
    except Exception as e:
        raise
