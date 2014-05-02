import RPi.GPIO as GPIO, time, os, random, datetime, sys
import argparse
from subprocess import Popen, PIPE, STDOUT
import glob

DEBUG = False

LEDCount = 19

class RGB:
	r = 0xFF
	g = 0xFF
	b = 0xFF
	def __init__(self, r, g, b):
		self.b = b
		self.r = r
		self.g = g

	def GetVal(self):
		return ((self.b & 0xFF) << 16) | ((self.r & 0xFF) << 8) | (self.g & 0xFF)


class LedStrip:
	spidev = None
	height = LEDCount

	def __init__(self):
		self.spidev = file("/dev/spidev0.0", "w")

	def WriteStrip(self, pixels):
		if len(pixels) != self.height:
		   return
		start = 0
		end = self.height
		for pixel in range(start,end):
			self.spidev.write( chr((pixels[pixel].GetVal() >> 16) & 0xff ))
			self.spidev.write( chr((pixels[pixel].GetVal() >> 8) & 0xff ))
			self.spidev.write( chr((pixels[pixel].GetVal()) & 0xff ))
		self.spidev.flush()

if __name__ == "__main__":

	subproc = None
	strip = LedStrip()
	startVal = 0
	endVal = 255
	step = 1
	pixelArr = []

	parser = argparse.ArgumentParser(description='Play an mp3 file using mpg321 and flicker the mouth LEDs at the same time.')
	parser.add_argument('soundclip', metavar='file', type=argparse.FileType('r'), nargs='?', help='A file to play.')
	args = parser.parse_args()
	if args.soundclip == None:
		parser.print_help()
		sys.exit()

	## Reset array
	for i in range(0,LEDCount,step):
		pixelArr.append(RGB(0,0,0));

	## Setup default pixels
	##
   	## "Mole pixel"
	pixelArr[8] = RGB(0,0,0)
	## Left Eye
	for pixel in range(9,13,step):
		if DEBUG:
			print "Writing pixel", pixel
		pixelArr[pixel] = RGB(0,255,0)
	## Third Eye/Nose
	pixelArr[13] = RGB(0,0,0)
	## Right Eye
	for pixel in range(14,18,step):
		if DEBUG:
			print "Writing pixel", pixel
		pixelArr[pixel] = RGB(0,255,0)
	for pixel in range(0,len(pixelArr),step):
		if DEBUG:
			print "Writing pixel", pixel

	cmd = ['/usr/bin/mpg321']
	cmd.append(args.soundclip.name)

	###print args.soundclip.name
	###sys.exit()

	subproc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)

	running = None

	time.sleep(0.18)

	while running == None:
		## Check if we're still playing
		running = subproc.poll()

		if DEBUG:
			print "subproc:", subproc
			print "running:", running

		speak = random.randint(0,25)

		if speak == 25:
			## Mouth - Lower
			for pixel in range(0,4,step):
				if DEBUG:
					print "Writing pixel", pixel
				pixelArr[pixel] = RGB(255,0,0)
			## Mouth - Upper
			for pixel in range(4,8,step):
				if DEBUG:
					print "Writing pixel", pixel
				pixelArr[pixel] = RGB(255,0,0)
			time.sleep(1/speak)
		else:
			for pixel in range(0,8,step):
				pixelArr[pixel] = RGB(0,0,0)

		strip.WriteStrip(pixelArr)


	for pixel in range(0,8,step):
		pixelArr[pixel] = RGB(0,0,0)

	strip.WriteStrip(pixelArr)
