from machine import I2S
from machine import Pin
import time
import struct

record_pin = Pin(23, Pin.IN, Pin.PULL_DOWN)

# Function to write a WAV file header
def write_wav_header(file, num_channels, sample_rate, bits_per_sample, data_size):
    file.write(b'RIFF')
    file.write(struct.pack('<I', 36 + data_size))
    file.write(b'WAVE')
    file.write(b'fmt ')
    file.write(struct.pack('<IHHIIHH', 16, 1, num_channels, sample_rate, sample_rate * num_channels * bits_per_sample // 8, num_channels * bits_per_sample // 8, bits_per_sample))
    file.write(b'data')
    file.write(struct.pack('<I', data_size))

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

with open("test.wav", "wb") as file:
    # Write WAV file header
    write_wav_header(file, num_channels=1, sample_rate=16000, bits_per_sample=16, data_size=0)
    
    while record_pin.value() == 1:
        read_bytes = audio_in.readinto(samples)
        # amplify the signal to make it more audible
        I2S.shift(buf=samples, bits=16, shift=4)
        file.write(samples[:read_bytes])

# Update WAV file header with actual data size
with open("test.wav", "r+b") as file:
    file.seek(40)
    file.write(struct.pack('<I', file.tell() - 44))

print("Finished Recording")
