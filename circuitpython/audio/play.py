import audiocore
import audiopwmio
import board
import array
import time
import adafruit_wave
import math
import struct
import pwmio
from audiocore import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!
#speaker = pwmio.PWMOut(board.A1)

length = 8000
sine_wave = array.array("H", [0] * (length))
audio_input = None
speaker = audiopwmio.PWMAudioOut(board.A1)
conversion_factor = 3.3/4096
file = adafruit_wave.open("CantinaBand3.wav", "rb")
file.setpos(0)
audio_input = file.readframes(length)

print(audio_input[0], audio_input[1])
print(audio_input[0].to_bytes(1, 'big'), audio_input[1].to_bytes(1, 'big'))
print((audio_input[1].to_bytes(1, 'big')[0] << 8) | audio_input[0].to_bytes(1, 'big')[0])

#wave_file = open("CantinaBand3.wav", "rb")
#wave = audiocore.WaveFile(wave_file)
#audio = AudioOut(board.A1)
#while True:
#    audio.play(wave)
#
#    # This allows you to do other things while the audio plays!
#    t = time.monotonic()
#    while time.monotonic() - t < 6:
#        pass
#
#    audio.pause()
#    print("Waiting for button press to continue!")
#    while button.value:
#        pass
#    audio.resume()
#    while audio.playing:
#        pass

while True:
    for i in range(0, length*2-1, 2):
        combined_byte = (audio_input[i].to_bytes(1, 'big')[0] << 8) | audio_input[i+1].to_bytes(1, 'big')[0]
        #combined_byte = 65000
        sine_wave[i//2] = int(combined_byte)
        #speaker.duty_cycle = combined_byte
        
    wave = audiocore.RawSample(sine_wave, sample_rate=8000)
    #speaker.play(wav, loop=True)
    
    while True:
        speaker.play(wave)
        t = time.monotonic()
        while time.monotonic() - t < 6:
            pass
        while speaker.playing:
            pass
#file.close()
#speaker.stop()


