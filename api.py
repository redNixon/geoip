from sanic import Sanic
from sanic.response import json
from core import utils

app = Sanic()

@app.route("/")
async def index(request):
    remote_addr, remote_port = request.ip
    return(json(utils.get_profile(remote_addr)))

@app.route("/<ip>")
async def geo_ip(request, ip):
    return(json(utils.get_profile(ip)))

@app.route("/bulk" , methods=["POST"])
async def bulk_geo_ip(request):
    ip_list = request.json
    results = []
    for ip in ip_list:
        results.append(utils.get_profile(ip))

    return(json(results))

@app.route("/<ip>/<field>")
async def return_ip_profile(request, ip, field = None):
    profile = utils.get_profile(ip)

    if not field:
        return(json(profile))
    else:
        return(json( profile.get( field ) ))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
