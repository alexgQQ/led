# Adafruit NeoPixel library port to the rpi_ws281x library.
# Author: Tony DiCola (tony@tonydicola.com), Jeremy Garff (jer@jers.net)
import atexit
import numpy as np
import _rpi_ws281x as ws


def Color(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (green << 16)| (red << 8) | blue


class _LED_Data(object):
    """Wrapper class which makes a SWIG LED color data array look and feel like
    a Python list of integers.
    """
    def __init__(self, channel, size):
        self.size = size
        if isinstance(size, tuple):
            self.width, self.height = self.size
        self.channel = channel

    def __getitem__(self, index):
        def get_pixel(x, y):
            pos = self.map_pixel(x, y)
            return ws.ws2811_led_get(self.channel, pos)

        if isinstance(index, slice):
            try:
                # TODO: Only full slice available
                rows = []
                for x in range(self.width):
                    col = []
                    for y in range(self.height):
                        col.append(get_pixel(x, y))
                    rows.append(col)
                return np.array(rows)
            except (Exception,) as error:
                print('LED wrapper failed with {}'.format(error))

        if isinstance(index, tuple):
            try:
                # TODO: Only single index available
                x, y = index
                return get_pixel(x, y)
            except (Exception,) as error:
                print('LED wrapper failed with {}'.format(error))

    def __setitem__(self, index, value):
        def set_pixel(x, y, value):
            pos = self.map_pixel(x, y)
            ws.ws2811_led_set(self.channel, pos, int(value))

        if isinstance(index, slice):
            try:
                # TODO: Only full slice available
                for x in range(self.width):
                    for y in range(self.height):
                        set_pixel(x, y, value[x, y])
            except (Exception,) as error:
                print('LED wrapper failed with {}'.format(error))

        if isinstance(index, tuple):
            try:
                # TODO: Only single index available
                x, y = index
                set_pixel(x, y, value)
            except (Exception,) as error:
                print('LED wrapper failed with {}'.format(error))

    def map_pixel(self, x, y):
        """
        Convert coordinates to stream for led strip
        Note: the current C code treats the led as a strip and not a matrix
        """
        pos = (x * self.height) - 1
        if pos < 0:
            pos = 0
        if x % 2:
            pos += self.height - y
        elif x == 0:
            pos += y
        else:
            pos += y + 1
        if pos < 0:
            pos = 0
        return pos


class Adafruit_NeoPixel(object):
    def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False,
            brightness=255, channel=0, strip_type=ws.WS2811_STRIP_RGB):
        """Class to represent a NeoPixel/WS281x LED display.  Num should be the
        number of pixels in the display, and pin should be the GPIO pin connected
        to the display signal line (must be a PWM pin like 18!).  Optional
        parameters are freq, the frequency of the display signal in hertz (default
        800khz), dma, the DMA channel to use (default 10), invert, a boolean
        specifying if the signal line should be inverted (default False), and
        channel, the PWM channel to use (defaults to 0).
        """
        # Create ws2811_t structure and fill in parameters.
        if isinstance(num, tuple):
            self.size = num
            self.width = num[0]
            self.height = num[1]
            num = num[0] * num[1]
        self._leds = ws.new_ws2811_t()

        # Initialize the channels to zero
        for channum in range(2):
            chan = ws.ws2811_channel_get(self._leds, channum)
            ws.ws2811_channel_t_count_set(chan, 0)
            ws.ws2811_channel_t_gpionum_set(chan, 0)
            ws.ws2811_channel_t_invert_set(chan, 0)
            ws.ws2811_channel_t_brightness_set(chan, 0)

        # Initialize the channel in use
        self._channel = ws.ws2811_channel_get(self._leds, channel)
        ws.ws2811_channel_t_count_set(self._channel, num)
        ws.ws2811_channel_t_gpionum_set(self._channel, pin)
        ws.ws2811_channel_t_invert_set(self._channel, 0 if not invert else 1)
        ws.ws2811_channel_t_brightness_set(self._channel, brightness)
        ws.ws2811_channel_t_strip_type_set(self._channel, strip_type)

        # Initialize the controller
        ws.ws2811_t_freq_set(self._leds, freq_hz)
        ws.ws2811_t_dmanum_set(self._leds, dma)

        # Grab the led data array.
        self._led_data = _LED_Data(self._channel, self.size)

        # Substitute for __del__, traps an exit condition and cleans up properly
        atexit.register(self._cleanup)

    def _cleanup(self):
        # Clean up memory used by the library when not needed anymore.
        if self._leds is not None:
            ws.delete_ws2811_t(self._leds)
            self._leds = None
            self._channel = None

    def begin(self):
        """Initialize library, must be called once before other functions are
        called.
        """
        resp = ws.ws2811_init(self._leds)
        if resp != ws.WS2811_SUCCESS:
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))

    def show(self):
        """Update the display with the data from the LED buffer."""
        resp = ws.ws2811_render(self._leds)
        if resp != ws.WS2811_SUCCESS:
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

    def setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        self._led_data[n] = color

    def setPixelColorRGB(self, n, red, green, blue, white = 0):
        """Set LED at position n to the provided red, green, and blue color.
        Each color component should be a value from 0 to 255 (where 0 is the
        lowest intensity and 255 is the highest intensity).
        """
        self.setPixelColor(n, Color(red, green, blue, white))

    def setBrightness(self, brightness):
        """Scale each LED in the buffer by the provided brightness.  A brightness
        of 0 is the darkest and 255 is the brightest.
        """
        ws.ws2811_channel_t_brightness_set(self._channel, brightness)

    def getBrightness(self):
        """Get the brightness value for each LED in the buffer. A brightness
        of 0 is the darkest and 255 is the brightest.
        """
        return ws.ws2811_channel_t_brightness_get(self._channel)

    def getPixels(self):
        """Return an object which allows access to the LED display data as if
        it were a sequence of 24-bit RGB values.
        """
        return self._led_data

    def numPixels(self):
        """Return the number of pixels in the display."""
        return ws.ws2811_channel_t_count_get(self._channel)

    def getPixelColor(self, n):
        """Get the 24-bit RGB color value for the LED at position n."""
        return self._led_data[n]

    def clear(self):
        self._led_data[:] = np.zeros(self.size)
        self.show()
