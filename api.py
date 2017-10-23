from sanic import Sanic
from sanic.response import json
from core import utils

app = Sanic()

@app.route("/")
async def index(request):
    remote_addr, remote_port = request.ip
    try:
        return(json(utils.get_profile(remote_addr)))
    except Exception:
        return(json({ "message" : "Error checking your ip."}))

@app.route("/<ip>")
async def geo_ip(request, ip):
    try:
        return(json(utils.get_profile(ip)))
    except Exception:
        return(json({ "message" : "Error checking your ip."}))

@app.route("/bulk" , methods=["POST"])
async def bulk_geo_ip(request):
    try:
        ip_list = request.json
        if type(ip_list) is list:
            results = []
            for ip in ip_list:
                results.append(utils.get_profile(ip))
            return(json(results))
        else:
            return(json( {"message" : "Invalid list."} ))

    except Exception:
        return(json({ "message" : "error checking your list."}))

@app.route("/<ip>/<field>")
async def return_ip_profile(request, ip , field):
    try:
        profile = utils.get_profile(ip)
        if field in profile:
            return(json( profile.get( field ) ))
        else:
            return(json( { "message" : "The field %s doesn't exist in data." % (field) } ))

    except Exception:
        return(json({ "message" : "Error checking your ip."}))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
