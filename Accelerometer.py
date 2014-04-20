from twisted.internet.serialport import SerialPort
from twisted.internet import protocol, reactor, defer
from twisted.internet.protocol import ClientCreator
from twisted.protocols import basic

class AccelerometerProtocol(basic.LineReceiver):
	def lineReceived(self, line):
		spl_str = str(line).split(' ')
		if (len(spl_str) != 3):
			return
		# Put in try catch statement if we get garbage
		try:
			x = int(spl_str[0])
			y = int(spl_str[1])
			z = int(spl_str[2])
		except Exception as e:
			return
		self.factory.newValues(x,y,z)

class AccelerometerFactory(protocol.ClientFactory):
	x = 0;
	y = 0;
	z = 0;
	protocol = AccelerometerProtocol
	callback = None

	def setCallback(self, callback):
		self.callback = callback

	def getLatest(self):
		return {'x':x,'y':y,'z':z}

	def newValues(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		if (self.callback):
			self.callback(x,y,z)

class Accelerometer:
	factory = None
	serialport = None

	def __init__(self, reactor, addr):
		self.factory = AccelerometerFactory()
		self.serialport = SerialPort(self.factory.buildProtocol(addr), addr, reactor, baudrate=115200)

	def setCallback(self, callback):
		self.factory.setCallback(callback)
	def getLatest():
		return self.factory.getLatest()

if __name__ == "__main__":
	addr = "/dev/ttyACM0"
	factory = AccelerometerFactory()
	reactor.run()