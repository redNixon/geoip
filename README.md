GeoIP API
=========

The GeoIP API leverages the free maxmind IP data to display information about IPs in an HTTP API mechanism.

Installation
============

Requirements
------------
* Python 3.5+
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)

After cloning the application repository simply run

```
$ make
```

To obtain the necessary dependencies and max-mind geoip data.

To run the API use

```
$ make run
```

API Endpoints
=============

```
GET localhost:7000/

Retrieve an IP profile about the remote host contacting the API.
```

```
GET localhost:7000/<ip>

Retrieve an IP profile about any IP
```

```
GET localhost:7000/<ip>/<field>

Retrieve a specific field of the profile.
```


```
POST localhost:7000/bulk

Retreive a list of profiles on IPs

# BODY
[ip1, ip2, ip3, ..., ipN]
```