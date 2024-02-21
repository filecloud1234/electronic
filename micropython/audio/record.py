from machine import I2S
from machine import Pin
import time

record_pin = Pin(23, Pin.IN, Pin.PULL_DOWN)


def wait_for_button():
    while record_pin.value() == 0:
        time.sleep_ms(100)
    time.sleep_ms(100)


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

print("Press and hold button to record")

wait_for_button()

print("Recording")

samples = bytearray(2048)

with open("test.raw", "wb") as file:
    while record_pin.value() == 1:
        read_bytes = audio_in.readinto(samples)
        # amplify the signal to make it more audible
        I2S.shift(buf=samples, bits=16, shift=4)
        file.write(samples[:read_bytes])

print("Finished Recording")

print("Processing data")
