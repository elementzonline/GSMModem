'''
Instructions

The comport used here is the audio comport. In windows user should install the drivers to get this comport 

This script contains test functions for testing the USBAudio functionality of SIM7600
'''

import serial
import time
import sys

PORT = '/dev/ttyUSB4'
baud = 115200

'''
# command to convert the wav file compatible with on call voice 

# sox -S input.wav output.wav channels 1 rate -L -s 8000

# AT commmand
# AT+CCMXPLAYWAV="D:/output.wav",1
# AT+CCMXSTOPWAV

# Voice call recording, use the below AT command to start recording to SDcard when on call
# AT+CREC=2,"D:/record.wav"

# stop voice recording
# AT+CREC=0
'''
 
def savefile(filename="raw.raw"):
    '''
    save the usb audio data to file. 
    Audacity is a great tool to analyse the saved raw data
    In Audacity --> File-->Import-->Rawdata
                    Settings - 8000Hz, 16 bit signed, Mono channel
    '''
    gsm_audio_serial.flushInput()
    gsm_audio_serial.flushOutput()
    seconds_elapsed = 0
    with open(filename, "ab") as f:
        while True:
            response = gsm_audio_serial.read(1)  # comment this line if echo off
            # print(response)
            # file = open(filename,'ba')
            if len(response) > 0:
                f.write(response)


def redirecttopipe():
    '''
    redirect the data from the usbAudio to stdout.
    In linux sox can be used to play the audio in realtime. Use the command below
    $ python usb_audio_test.py | play -r 8000 -c 1 -t raw -e signed-integer -b 16 -
    '''
    gsm_audio_serial.flushInput()
    gsm_audio_serial.flushOutput()
    seconds_elapsed = 0
    while True:
        response = gsm_audio_serial.read(1)  # comment this line if echo off
        # import sys
        sys.stdout.write(response)


def echotest():
    '''
    used to quickly test the usb audio interface by echoing the audio data back to the USBAudio serial port.
    Thus the user can hear back the voice at the caller end after attending the call 
    and enabling the USBAudio channel
    '''
    gsm_audio_serial.flushInput()
    gsm_audio_serial.flushOutput()
    seconds_elapsed = 0
    while True:
        response = gsm_audio_serial.read(100)  # comment this line if echo off
        # import sys
        # response = "Hai"
        # sys.stdout.write(response)
        gsm_audio_serial.write(response)


# print("Trying with baudrate {}".format(baud))

gsm_audio_serial = serial.Serial()
gsm_audio_serial.port = PORT
gsm_audio_serial.baudrate = baud
gsm_audio_serial.timeout = 0
gsm_audio_serial.xonxoff = False
gsm_audio_serial.rtscts = False
# gsm_audio_serial.dsrdtr = False
# gsm_audio_serial.rts = True
# gsm_audio_serial.dtr = True
gsm_audio_serial.bytesize = serial.EIGHTBITS
gsm_audio_serial.parity = serial.PARITY_NONE
gsm_audio_serial.stopbits = serial.STOPBITS_ONE

try:
    gsm_audio_serial.open()
    gsm_audio_serial.flushInput()
    gsm_audio_serial.flushOutput()
except:
    print ('Cannot open serial port')
    sys.exit()


if __name__ == '__main__':
    # save the serial data to file
    # savefile("rawdata.data")

    # redirect the serial data to stdout
    # redirecttopipe()   # python usb_audio_test.py | play -r 8000 -c 1 -t raw -e signed-integer -b 16  -

    # send the serial data back so that the audio is echoed at caller end
    echotest()