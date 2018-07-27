#!/usr/bin/env python

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

print "# RFID Wipe\n"

print "Waiting for tag...\n"

while True:

    sector = 1

    while True:

        (status, TagSize) = RFID.Request(RFID.PICC_REQIDL)

        if status != RFID.MI_OK:
            continue

        if sector >= TagSize:
            break

        print "Wiping sector", sector, "..."

        # Selecting blocks
        BlockAddrs = [ (sector * 4), (sector * 4 + 1), (sector * 4 + 2) ]
        TrailerBlockAddr = (sector * 4 + 3)

        # Writing data
        (status, UID) = RFID.Anticoll()

        if status != RFID.MI_OK:
            break

        RFID.SelectTag(UID)
        status = RFID.Auth(RFID.PICC_AUTHENT1A, TrailerBlockAddr, KEY, UID)
        if status == RFID.MI_OK:
            data = bytearray()
            data.extend(bytearray("".ljust(len(BlockAddrs) * 16)))
            i = 0
            for block_num in BlockAddrs:
                RFID.Write(block_num, data[(i*16):(i+1)*16])
                i += 1
            print "Sector", sector, "wiped!"
        else:
            print "Can't access sector", sector, "!"
        RFID.StopCrypto1()
        sector += 1

    print "\nTag wiped!"
    break

GPIO.cleanup()