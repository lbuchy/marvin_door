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
           self.spidev.write( chr((pixels[pixel].b >> 16) & 0xff ))
           self.spidev.write( chr((pixels[pixel].b >> 8) & 0xff ))
           self.spidev.write( chr((pixels[pixel].b) & 0xff ))
           #self.spidev.write( chr(pixels[pixel].g >> 8) & 0xff )
           #self.spidev.write( chr(pixels[pixel].r >> 0) & 0xff )
        self.spidev.flush()

if __name__ == "__main__":
    strip = LedStrip()
    startVal = 0
    endVal = 255
    step = 1
    for val in range(startVal, endVal, step):
        pixelArr = [RGB(val,val,val)] * 10
        strip.WriteStrip(pixelArr)
        time.sleep(0.05)
