import wifi
import os
import ipaddress
import socketpool
import wifi
import board
from adafruit_httpserver import Server, Request, Response, FileResponse, POST
#import storage 
import digitalio
#storage.remount("/static", readonly=False)
ap_ssid = "Poulstar"
ap_password = "12345678"

ipv4 =  ipaddress.IPv4Address("192.168.4.1")
netmask =  ipaddress.IPv4Address("255.255.255.0")
gateway =  ipaddress.IPv4Address("192.168.1.1")
wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)

state = wifi.radio.ap_active
print(state)

print("Access point created with SSID: {}, password: {}".format(ap_ssid, ap_password))

print("My IP address is", wifi.radio.ipv4_gateway_ap)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/", debug=True)


@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return FileResponse(request, "index.html", "/")
    #return Response(request, "Hello from the CircuitPython HTTP Server!")

@server.route("/upload", [POST])
def upload(request: Request):
    if request.method == POST:
        file = request.form_data.files.get("myfile")

        #with open("hello.txt", "wb") as f:
        print(file.content_bytes)
server.serve_forever(str(wifi.radio.ipv4_gateway_ap))
