#!/usr/bin/env python
import RPi.GPIO as GPIO
import MFRC522

# Keys
DEFAULT_KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

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

print "# RFID Reader\n"
print "Info: Leave the sector field empty to exit.\n"

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

        # Reading data
        BlockAddrs = [ (sector * 4), (sector * 4 + 1), (sector * 4 + 2) ]
        TrailerBlockAddr = (sector * 4 + 3)
        status = RFID.Auth(RFID.PICC_AUTHENT1A, TrailerBlockAddr, KEY, UID)
        data = []
        text_read = ""
        if status == RFID.MI_OK:
            for block_num in BlockAddrs:
                block = RFID.Read(block_num) 
                if block:
                    data += block
            if data:
                text_read = "".join(chr(i) for i in data)
            print "UID:  ", uid_to_num(UID)
            print "Data: ", text_read,"\n"
        else:
            print "Can't access sector", sector, "!\n"
        RFID.StopCrypto1()

        WaitingForTag = False

GPIO.cleanup()