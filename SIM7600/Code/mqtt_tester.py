import serial
import time
import sys

PORT = 'COM31'
baud = 115200

def sendCommand(at_com):
    print(time.time(),"send:",at_com)
    gsm_serial.flushInput()
    gsm_serial.flushOutput()
    # gsm_serial.write('\n')
    gsm_serial.write(at_com + '\r')

 
def getResponse(required_response="",timeout_in_seconds=10):
    gsm_serial.flushInput()
    gsm_serial.flushOutput()
    seconds_elapsed = 0
    while seconds_elapsed < timeout_in_seconds:
        response = gsm_serial.readline().rstrip()  # comment this line if echo off
        if (len(response)) > 0:
            print(time.time(),"recv:",response)
            if response == required_response:
                return True
        seconds_elapsed = seconds_elapsed+1
    return False



print("Trying with baudrate {}".format(baud))

gsm_serial = serial.Serial()
gsm_serial.port = PORT
gsm_serial.baudrate = baud
gsm_serial.timeout = 1
gsm_serial.xonxoff = False
gsm_serial.rtscts = False
gsm_serial.bytesize = serial.EIGHTBITS
gsm_serial.parity = serial.PARITY_NONE
gsm_serial.stopbits = serial.STOPBITS_ONE

try:
    gsm_serial.open()
    gsm_serial.flushInput()
    gsm_serial.flushOutput()
except:
    print ('Cannot open serial port')
    sys.exit()

status = False
while not status:
    status = False
    sendCommand("ATE0")
    status = getResponse("OK",5)

sendCommand("AT+CMQTTDISC=0,60")
status = getResponse("OK",5)

sendCommand("AT+CMQTTREL=0")
status = getResponse("OK",5)

sendCommand("AT+CMQTTSTOP")
status = getResponse("OK",5)

status = False
while not status:
    status = False
    sendCommand("AT+CMQTTSTART")
    status = getResponse("+CMQTTSTART: 0",6)

status = False
while not status:
    status = False
    sendCommand('AT+CMQTTACCQ=0,"elementz123"')
    status = getResponse("OK",10)

status = False
while not status:
    status = False
    sendCommand('AT+CMQTTCONNECT=0,"tcp://iot.eclipse.org:1883",90,1,"",""')
    status = getResponse("+CMQTTCONNECT: 0,0",20)

status = False
while not status:
    status = False
    topic = "mqtt/sim7600"
    sendCommand('AT+CMQTTTOPIC=0,{}'.format(len(topic)))
    time.sleep(1)
    sendCommand(topic)
    status = getResponse("OK",2)


status = False
while not status:
    status = False
    payload = "hello"
    sendCommand('AT+CMQTTPAYLOAD=0,{}'.format(len(payload)))
    time.sleep(1)
    sendCommand(payload)
    status = getResponse("OK",2)

status = False
while not status:
    status = False
    sendCommand("AT+CMQTTPUB=0,1,60")
    status = getResponse("+CMQTTPUB: 0,0",20)


sendCommand("AT+CMQTTDISC=0,60")
status = getResponse("OK",5)

sendCommand("AT+CMQTTREL=0")
status = getResponse("OK",5)

sendCommand("AT+CMQTTSTOP")
status = getResponse("OK",5)