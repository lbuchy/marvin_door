import RPi.GPIO as GPIO, time, os

class RGB:
    r = 0xff
    g = 0xff
    b = 0xff
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class LedStrip:
    spidev = None
    height = 10

    def __init__(self):
        self.spidev = file("/dev/spidev0.0", "w")

    def WriteStrip(self, pixels):
        if len(pixels) != self.height:
           return
        start = 0
        end = self.height
        step = 1
        for pixel in range(start,end,step):
           self.spidev.write( chr((pixels[pixel].b) & 0xff ))
           self.spidev.write( chr((pixels[pixel].r) & 0xff ))
           self.spidev.write( chr((pixels[pixel].g) & 0xff ))
        self.spidev.flush()

if __name__ == "__main__":
    strip = LedStrip()
    startVal = 0
    endVal = 255
    step = 1
    while True:
    	for val in range(startVal, endVal, step):
    	    pixelArr = [RGB(255 - val,val,127)] * 10
    	    strip.WriteStrip(pixelArr)
    	    time.sleep(0.0001)
