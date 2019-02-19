import serial

ser=serial.Serial("/dev/ttyUSB0",115200,timeout=0.5)

ser.write('get high')

ser.inWaiting()

print(ser.read(6))
