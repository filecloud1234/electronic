# Complete project details at https://RandomNerdTutorials.com

try:
  import usocket as socket
except:
  import socket
from machine import I2S
from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MicroPython-AP'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

spk_bck_pin = Pin(19)
spk_ws_pin = Pin(27)
spk_sdout_pin = Pin(18)

audio_out = I2S(
    1,
    sck=spk_bck_pin,
    ws=spk_ws_pin,
    sd=spk_sdout_pin,
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO,
    rate=16000,
    ibuf=20000,
)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"</head><body><h1>Hello, World!</h1></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
f=open("audio.raw","wb")
while True:
  conn, addr = s.accept()
  #print('Got a connection from %s' % str(addr))
  while True:
    data = conn.recv(2048)
    f.write(data)
    try:
        if data.decode() == '':
            print("bye")
            break
    except:
        pass
    
   
  samples = bytearray(2048)
  with open("audio.raw", "rb") as file:
    samples_read = file.readinto(samples)
    while samples_read > 0:
        audio_out.write(samples[:samples_read])
        samples_read = file.readinto(samples)
  conn.close()
