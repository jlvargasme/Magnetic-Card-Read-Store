# Magnetic-Card-Read-Store
Reads information from magnetic reader and stores locally in a csv

Created by: jlvargasme  
Modified by: evaneidt  

## Setup
Run the following:
```
python3 -m venv env
pip install -r requirements.txt
```

Install libusb-win32 drivers: **https://sourceforge.net/projects/libusb-win32/**

## Run
Follow the Setup instructions, connect the card reader, then run the following:
```
& python3 main.py
```

## Run Files 
### main.py
Runs the main card reader code. Based on peripheral.py and reader.py from Test Files.  

## Test Files 
### serial_ports.py
Lists connected serial devices.

### peripheral.py
Reads from the MSR90 MagStripe reader USB device.  
Prints string read from a card's magstripe to stdout.

### reader.py
Reads from stdin to **students.csv**.  
Format (that we care about): *--------UMID&Last/First&uniqname*
