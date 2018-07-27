#!/usr/bin/env python

#!/usr/bin/env python
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import sys

# Keys
DEFAULT_KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
KEY_S0 = [0x20, 0x20, 0x20, 0x20, 0x20, 0x20]

# Selecting key
KEY = DEFAULT_KEY

MainLoop = True
WaitingForTag = True

def uid_to_num(uid):
    n = 0
    for i in range(0, 5):
        n = n * 256 + uid[i]
    return n

RFID = MFRC522.MFRC522()

# Get tag size if available
(status, TagSize) = RFID.Request(RFID.PICC_REQIDL)

while MainLoop:
    if TagSize > 0:
        message = "Sector [1 - %s]: " % TagSize
    else:
        message = "Sector: "

    try:
        sector = input(message)
    except:
        MainLoop = False
        continue
    else:
        try:
            text = raw_input("Data: ")
        except:
            continue
        else:
            if status != RFID.MI_OK:
                print "Waiting for Tag...\n"
            else:
                print ""
            WaitingForTag = True

    while WaitingForTag:
        (status, TagSize) = RFID.Request(RFID.PICC_REQIDL)

        if status != RFID.MI_OK:
            continue

        if sector < 1 or sector > (TagSize - 1):
            print "Sector out of range (1 - %s)\n" % (TagSize - 1)
            WaitingForTag = False
            continue

        (status, UID) = RFID.Anticoll()

        if status != RFID.MI_OK:
            continue

        RFID.SelectTag(UID)

        # Selecting blocks
        BlockAddrs = [ (sector * 4), (sector * 4 + 1), (sector * 4 + 2) ]
        TrailerBlockAddr = (sector * 4 + 3)

        # Writing data
        status = RFID.Auth(RFID.PICC_AUTHENT1A, TrailerBlockAddr, KEY, UID)
        if status == RFID.MI_OK:
            data = bytearray()
            data.extend(bytearray(text.ljust(len(BlockAddrs) * 16)))
            i = 0
            for block_num in BlockAddrs:
                RFID.Write(block_num, data[(i*16):(i+1)*16])
                i += 1
            print "UID:  ", uid_to_num(UID)
            print "Data: ", text[0:(len(BlockAddrs) * 16)], "\n"
        else:
            print "Can't access sector", sector, "!\n"
        RFID.StopCrypto1()

        WaitingForTag = False

GPIO.cleanup()