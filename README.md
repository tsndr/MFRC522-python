# MFRC522-python

Reading and Writing MiFare tags using a Raspberry Pi and the RFID-RC522.

## Usage
Run one of these commands and follow the instructions:

#### Reading a tag
```
python read.py
```

#### Writing a tag
```
python write.py
```

#### Resetting a tag
```
python wipe.py
```

## Installation

### Enable SPI
Open the configuration using this command:
```
sudo raspi-config
```
In the menu select `5 Interfacing options`, then enable `P4 SPI` and reboot.

### Wiring
Connect the RC522's Pins to the RaspberryPi's GPIO pins.

RC522 | RaspberryPi
----- | ----------:
SDA   | 24
SCK   | 23
MOSI  | 19
MISO  | 21
IRQ   | -
GND   | 6
RST   | 22
3.3V  | 1

Dont connect the IRQ pin.

For a detailed pinout plan check [this website](https://pinout.xyz/).

### Install dependencies
First of all we need to install the `git` and `python-dev` package using this command:
```
sudo apt install git python-dev -y
```
Now we have to install `SPI-Py` using the folowing commands:
```
cd ~
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py/
sudo python setup.py install
```

### Install MFRC522-python
Almost done, just a few commands left to install this package:
```
cd ~
git clone https://github.com/tsndr/MFRC522-python.git
cd MFRC522-python/
```
Everything set up, now you can start reading and writing RFID-Tags 😉