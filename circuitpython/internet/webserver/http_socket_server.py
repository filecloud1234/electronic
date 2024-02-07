from asyncio import create_task, gather, run, sleep as async_sleep
import microcontroller
import socketpool
import wifi
import ipaddress
from adafruit_httpserver import Server, Request, Response, Websocket, GET

ipv4 = ipaddress.IPv4Address("192.168.10.2")
netmask = ipaddress.IPv4Address("255.255.255.0")
gateway = ipaddress.IPv4Address("192.168.1.1")
wifi.radio.stop_ap()
wifi.radio.start_ap(ssid="PoloFruit", password="p12345678",
                    authmode=[wifi.AuthMode.WPA2], max_connections=20)
wifi.radio.set_ipv4_address_ap(ipv4=ipv4, netmask=netmask, gateway=gateway)
wifi.radio.stop_dhcp_ap()
wifi.radio.start_dhcp_ap()
print("WIFI AP up")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)
print("Websocket created")

websocket: Websocket = None

HTML_TEMPLATE = """
<html lang="en">
    <head>
        <title>Websocket Client</title>
    </head>
    <body>
        <p>CPU temperature: <strong>-</strong>&deg;C</p>
        <p>NeoPixel Color: <input type="color"></p>
        <script>
            const cpuTemp = document.querySelector('strong');
            const colorPicker = document.querySelector('input[type="color"]');

            let ws = new WebSocket('ws://192.168.10.2/connect-websocket');

            ws.onopen = () => console.log('WebSocket connection opened');
            ws.onclose = () => console.log('WebSocket connection closed');
            ws.onmessage = event => cpuTemp.textContent = event.data;
            ws.onerror = error => cpuTemp.textContent = error;

            colorPicker.oninput = debounce(() => ws.send(colorPicker.value), 200);

            function debounce(callback, delay = 1000) {
                let timeout
                return (...args) => {
                    clearTimeout(timeout)
                    timeout = setTimeout(() => {
                    callback(...args)
                  }, delay)
                }
            }
        </script>
    </body>
</html>
"""


@server.route("/client", GET)
def client(request: Request):
    print("request to client")
    return Response(request, HTML_TEMPLATE, content_type="text/html")


@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket  # pylint: disable=global-statement

    if websocket is not None:
        websocket.close()  # Close any existing connection

    websocket = Websocket(request)

    return websocket


print(str(ipv4))
server.start(str(ipv4))
print("socket is up")


async def handle_http_requests():
    while True:
        server.poll()

        await async_sleep(0.2)


async def handle_websocket_requests():
    while True:
        if websocket is not None:
            if (data := websocket.receive(fail_silently=True)) is not None:
                print(data)

        await async_sleep(0.1)


async def send_websocket_messages():
    while True:
        if websocket is not None:
            cpu_temp = round(microcontroller.cpu.temperature, 2)
            websocket.send_message(str(cpu_temp), fail_silently=True)

        await async_sleep(5)


async def main():
    await gather(
        create_task(handle_http_requests()),
        create_task(handle_websocket_requests()),
        create_task(send_websocket_messages()),
    )


run(main())
