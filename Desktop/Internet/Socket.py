
#pip install websocket-client
from websocket import create_connection

ws = create_connection("ws://192.168.10.2:80/connect-websocket")
print(ws.recv())
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()
