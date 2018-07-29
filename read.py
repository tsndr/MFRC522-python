#!/usr/bin/env python
import RPi.GPIO as GPIO
import MFRC522

# Keys
DEFAULT_KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

# Selecting key
KEY = DEFAULT_KEY

def uid_to_num(uid):
    n = 0
    for i in range(0, 5):
        n = n * 256 + uid[i]
    return n

RFID = MFRC522.MFRC522()

print "# RFID Reader\n"
print "Info: Leave the sector field empty to exit.\n"

# Get tag size if available
(Status, TagSize) = RFID.Request(RFID.PICC_REQIDL)

while True:

    if TagSize > 0:
        message = "Sector [1 - %s]: " % (TagSize - 1)
    else:
        message = "Sector: "

    try:
        Sector = input(message)
    except:
        print ""
        break
    else:
        print "Waiting for Tag...\n"

    while True:

        (Status, TagSize) = RFID.Request(RFID.PICC_REQIDL)

        if Status != RFID.MI_OK:
            continue

        if TagSize < 1:
            print("Can't read tag properly!")
            break

        if Sector < 1 or Sector > (TagSize - 1):
            print "Sector out of range (1 - %s)\n" % (TagSize - 1)
            break

        # Selecting blocks
        BaseBlockLength = 4
        if Sector < 32:
            BlockLength = BaseBlockLength
            StartAddr = Sector * BlockLength
        else:
            BlockLength = 16
            StartAddr = 32 * BaseBlockLength + (Sector - 32) * BlockLength

        BlockAddrs = []
        for i in range(0, (BlockLength - 1)):
            BlockAddrs.append((StartAddr + i))
        TrailerBlockAddr = (StartAddr + (BlockLength - 1))

        # Initializing tag
        (Status, UID) = RFID.Anticoll()

        if Status != RFID.MI_OK:
            break

        # Reading sector
        RFID.SelectTag(UID)
        Status = RFID.Auth(RFID.PICC_AUTHENT1A, TrailerBlockAddr, KEY, UID)
        data = []
        text_read = ""
        if Status == RFID.MI_OK:
            for block_num in BlockAddrs:
                block = RFID.Read(block_num) 
                if block:
                    data += block
            if data:
                text_read = "".join(chr(i) for i in data)
            print "UID:  ", uid_to_num(UID)
            print "Data: ", text_read,"\n"
        else:
            print "Can't access sector", Sector, "!\n"
        RFID.StopCrypto1()
        break

RFID.AntennaOff()
GPIO.cleanup()