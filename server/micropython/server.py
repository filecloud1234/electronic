import network

ap = network.WLAN(network.AP_IF)

ap.active(True)

ap.config(essid="Micropython", password="12345678")

print(ap.ifconfig())

from microdot import Microdot

app = Microdot()

@app.route('/')
def index(request):
    return 'Hello, world!'

if __name__ == "__main__":
    app.run()
