#!/usr/bin/env python
from __future__ import print_function
import RPi.GPIO as GPIO
import MFRC522

# Keys
DEFAULT_KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

# Selecting key
KEY = DEFAULT_KEY

RFID = MFRC522.MFRC522()

print("# RFID Wipe\n")

print("Waiting for tag...\n")

while True:

    Sector = 1

    while True:

        (Status, TagSize) = RFID.Request(RFID.PICC_REQIDL)

        if Status != RFID.MI_OK:
            continue

        if TagSize < 1:
            print("Can't read tag properly!")
            break

        if Sector >= TagSize:
            break

        # Only for formatting
        Spacer = ""
        if Sector < 10:
            Spacer = " "

        print("Wiping sector %s%s ... " % (Spacer, Sector), end="")

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

        # Wiping sector
        RFID.SelectTag(UID)
        Status = RFID.Auth(RFID.PICC_AUTHENT1A, TrailerBlockAddr, KEY, UID)
        if Status == RFID.MI_OK:
            data = bytearray()
            data.extend(bytearray("".ljust(len(BlockAddrs) * 16)))
            i = 0
            for block_num in BlockAddrs:
                RFID.Write(block_num, data[(i*16):(i+1)*16])
                i += 1
            print("OK!")
        else:
            print("NO ACCESS!")
        RFID.StopCrypto1()
        Sector += 1

    print("\nTag wiped!")
    break

GPIO.cleanup()