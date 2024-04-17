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

import asyncio
record_pin = Pin(23, Pin.IN, Pin.PULL_DOWN)


ssid = 'MicroPython-AP'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

mic_sck_pin = Pin(26)
mic_ws_pin = Pin(22)
mic_sd_pin = Pin(21)

audio_in = I2S(
    0,
    sck=mic_sck_pin,
    ws=mic_ws_pin,
    sd=mic_sd_pin,
    mode=I2S.RX,
    bits=16,
    format=I2S.MONO,
    rate=16000,
    ibuf=20000
)


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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

async def socket():
    print("socket")
    global conn, addr
    conn, addr = s.accept()
    print("connected")
    await asyncio.sleep_ms(1000)
  
async def record():
    print("record")
    while True:
        while record_pin.value() == 0:
            #print(record_pin.value())
            await asyncio.sleep_ms(200)
            
            
        print("hello")
        if conn == None:
            await asyncio.sleep_ms(100)
            continue
        f=open("audio.raw","wb")
        samples = bytearray(2048)
        while record_pin.value() == 1:
            print("recording")
            read_bytes = audio_in.readinto(samples)
            I2S.shift(buf=samples, bits=16, shift=2)
            f.write(samples[:read_bytes])
            
        f.close()
        f = open("audio.raw", "rb")
        
        print("while")
        while True:
            print("loop")
            chunk = f.read(2048)
            if chunk == b'':
                break
            conn.send(chunk)
        print("bye")
        conn.send(b'bye')
        f.close()

async def play():
    print("play")
    while True:
        if conn == None:
            await asyncio.sleep_ms(100)
            continue
        if conn.recv(4) == b'play':  
            f = open("audio.raw","wb")
            while True:
                data = conn.recv(2048)
                try:
                    if data.decode() == 'bye':     
                        print("bye")
                        break
                except:
                    pass
                f.write(data)
                
            f.close()
            print("playing")
            samples = bytearray(2048)
            with open("audio.raw", "rb") as file:
                samples_read = file.readinto(samples)
                while samples_read > 0:
                    audio_out.write(samples[:samples_read])
                    samples_read = file.readinto(samples)
                print("while end")
    

async def main():
    print("main")
    task1 = asyncio.create_task(socket())
    task2 = asyncio.create_task(record())
#    task3 = asyncio.create_task(play())
    
    await asyncio.gather(task1,task2)
asyncio.run(main())

