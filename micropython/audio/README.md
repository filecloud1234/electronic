# Recording Audio Using SPH0645 And ESP32 With Micropython

| ESP32 | SPH0645 | Button |
|:-----:|:-------:|:------:|
|  3v3  |   3v3   |    -   |
|  GND  |   GND   |   GND  |
|   26  |   BCLK  |    -   |
|   21  |   DOUT  |    -   |
|   22  |   LRCL  |    -   |
|   23  |    -    |   23   |

BCLK on the microphone is connected to the sck pin on the Pico.
DOUT on the microphone is connected to the sd pin on the Pico.
LRCLK on the microphone is connected to the ws pin on the Pico.
