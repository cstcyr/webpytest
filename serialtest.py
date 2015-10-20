import serial

s = serial.Serial(port='/dev/tty.usbmodem187', baudrate=57600)

while 1:
	line = s.readline()
	if line.startswith('1'):
		mySplit = line.split()
		BPM = mySplit[2]
		PS02 = mySplit[4]
		
		print BPM
		print PS02