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

