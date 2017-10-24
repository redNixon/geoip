from sanic import Sanic
from sanic.response import json
from core import utils
from aiocache.serializers import JsonSerializer
from aiocache import SimpleMemoryCache

app = Sanic()

cache = SimpleMemoryCache(namespace="geo_api_", serializer=JsonSerializer())

@app.route("/")
async def index(request):
    remote_addr, remote_port = request.ip
    cached_geo_ip = await cache.get(remote_addr)
    if cached_geo_ip is None:
        try:
            profile = utils.get_profile(remote_addr)
            await cache.set(remote_addr, profile)
            return(json(profile))
        except Exception:
            return(json({ "message" : "Error checking your ip."}))
    else:
        return(json(cached_geo_ip))

@app.route("/<ip>")
async def geo_ip(request, ip):
    cached_geo_ip = await cache.get(ip)
    if cached_geo_ip is None:
        try:
            profile = utils.get_profile(ip)
            await cache.set(ip, profile)
            return(json(profile))
        except Exception:
            return(json({ "message" : "Error checking your ip."}))

    else:
        return(json(cached_geo_ip))

@app.route("/bulk" , methods=["POST"])
async def bulk_geo_ip(request):
    try:
        ip_list = request.json
        if type(ip_list) is list:
            results = []
            for ip in ip_list:
                cached_geo_ip = await cache.get(ip)
                if cached_geo_ip is None:
                    try:
                        profile = utils.get_profile(ip)
                        await cache.set(ip, profile)
                        results.append(utils.get_profile(ip))
                    except Exception:
                        return(json({"message" :  "Error checking ip %s in your list." % (ip) }))
                else:
                    results.append(cached_geo_ip)
            return(json(results))
        else:
            return(json( {"message" : "Invalid list."} ))

    except Exception:
        return(json({ "message" : "error checking your list."}))

@app.route("/<ip>/<field>")
async def return_ip_profile(request, ip , field):
    try:
        cached_geo_ip = await cache.get(ip)
        if cached_geo_ip is None:
            profile = utils.get_profile(ip)
            await cache.set(ip, profile)
        else:
            profile = cached_geo_ip

        if field in profile:
            return(json( profile.get( field ) ))
        else:
            return(json( { "message" : "The field %s doesn't exist in data." % (field) } ))

    except Exception:
        return(json({ "message" : "Error checking your ip."}))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
