# EPNM Scripts

This set of scripts provide you with examples around how to get and change the network using Cisco Evolved Programmable Network Manager

Contacts:

* Santiago Flores (sfloresk@cisco.com)

## Instruction

Download the code to your computer
```
git clone https://github.com/sfloresk/epnm-scripts.git
```

Open the Constants.py file and replace the values with your credentials:

```
EPN_URL = "https://epnm.cisco.com/"
EPN_USER = "your_username"
EPN_PASSWORD = "your_password"
```

Go to the project directory and install python requirements with pip:
```
pip install -r requirements.txt
```

You are ready to go!

## Available Scripts
### Devices.py
This script gets devices and creates an excel file. You can filter the different devices using a paramater called query.

To change the parameter just open the Devices.py file and edit line #69

#### For example: 

Get all devices
```
getDevicesByType()
```

Get all NCS devices
```
getDevicesByType("*NCS*")
```

Get all ASR devices
```
getDevicesByType("*ASR*")
```

Get only the Cisco NCS 2006 devices:
```
getDevicesByType("Cisco NCS 2006")
```

#### To run this script:
```
python Devices.py
```

### Alarms.py
This script gets alarms and creates an excel file. You can filter the different devices using a paramater called query.

To change the parameter just open the Alarm.py file

#### For example: 

Get all devices
```
getAlarms()
```

#### To run this script:
```
python Alarms.py
```

### Menu.py
This script shows you a menu where you can get devices by type, name and group. It is also able to get all alarms
and to execute commands in devices. 

_In order to get the execution of the commands you need to have a CLI template called "custom_command" and have inside a 
variable called "command"_ in EPN-M


#### To run this script:
```
python menu.py
```

