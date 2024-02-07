import supervisor
import asyncio
import adafruit_wave
import struct
import storage
import board
import analogio
import sys
import time
# storage.remount("/", readonly=False)
import os
import board
import busio as io
import digitalio
import storage
import adafruit_sdcard
import microcontroller
from time import sleep
# Use any pin that is not taken by SPI
SD_CS = board.GP13
 
# Connect to the card and mount the filesystem.
spi = io.SPI(board.GP10, board.GP11, board.GP12)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

adc = analogio.AnalogIn(board.A0)
conversion_factor = 3.3/4096
buffer = []

f = adafruit_wave.open("/sd/audio.wav", "wb")
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(1900)


async def writer_job(data):
    global f
    f.writeframes(bytearray(data))
    print(time.monotonic())


async def recorder_job():
    global adc, conversion_factor, buffer
    print(time.monotonic())
    while True:
        sample = adc.value * conversion_factor
        frame = bytearray(struct.pack('>h', int(sample)))
        buffer.extend(frame)

        if len(buffer) > 1000:
            writer_task = asyncio.create_task(
                writer_job(buffer)
            )
            asyncio.gather(
                writer_task
            )
            buffer = []
            print("clear buffer")

        await asyncio.sleep(0)


async def main():
    recorder_task = asyncio.create_task(
        recorder_job()
    )
    await asyncio.gather(
        recorder_task
    )

try:
    asyncio.run(main())
except KeyboardInterrupt:
    f.close()
    sys.exit(0)

