import os

# Main driver settings

LED_MATRIX_CONFIG = dict(
    num=(32, 8),        # Size of LED pixels.
    pin=18,             # GPIO pin connected to the pixels (18 uses PWM! 10 uses SPI /dev/spidev0.0).
    freq_hz=800000,     # LED signal frequency in hertz (usually 800khz)
    dma=10,             # DMA channel to use for generating signal (try 10)
    brightness=150,     # Set to 0 for darkest and 255 for brightest
    invert=False,       # True to invert the signal (when using NPN transistor level shift)
    channel=0,          # set to '1' for GPIOs 13, 19, 41, 45 or 53
)

CLIENT_CONFIG = dict(
    PROTOCOL='http://',
    HOST='192.168.0.16',
    PORT=5000,
    ROUTE='/board',
)
