#!/usr/bin/env python

#!/usr/bin/env python
import RPi.GPIO as GPIO
import MFRC522
import signal

# Keys
DEFAULT_KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
KEY_S0 = [0x20, 0x20, 0x20, 0x20, 0x20, 0x20]

# Selecting key
KEY = DEFAULT_KEY

def uid_to_num(uid):
    n = 0
    for i in range(0, 5):
        n = n * 256 + uid[i]
    return n

MIFAREReader = MFRC522.MFRC522()

print "Waiting for tag...\n"

while True:

    sector = 1

    while True:

        (status, TagSize) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status != MIFAREReader.MI_OK:
            continue

        if sector >= TagSize:
            break

        print "Wiping sector", sector, "..."

        # Selecting blocks
        BlockAddrs = [ (sector * 4), (sector * 4 + 1), (sector * 4 + 2) ]
        TrailerBlockAddr = (sector * 4 + 3)

        # Writing data
        (status, UID) = MIFAREReader.MFRC522_Anticoll()

        if status != MIFAREReader.MI_OK:
            break

        MIFAREReader.MFRC522_SelectTag(UID)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, TrailerBlockAddr, KEY, UID)
        if status == MIFAREReader.MI_OK:
            data = bytearray()
            data.extend(bytearray("".ljust(len(BlockAddrs) * 16)))
            i = 0
            for block_num in BlockAddrs:
                MIFAREReader.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
                i += 1
            print "Sector", sector, "wiped!"
        else:
            print "Can't access sector", sector, "!"
        MIFAREReader.MFRC522_StopCrypto1()
        sector += 1

    print "\nTag wiped!"
    break

GPIO.cleanup()