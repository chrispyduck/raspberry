#Raspberry Pi-based vehicle black box

##Immediate goals
* Deactivate peripherals when vehicle is off
* Monitor vehicle status using OBDII port via ELM327 interface and store data in local MongoDB instance
* Utilize Bluetooth tethering to gain internet access when vehicle is on (phone provides access)
* Periodically upload locally recoded data to remote MongoDB instance (using MongoLab)

##Components
* Python-based controller/recording software; see [Blackberry](blackberry)
* Simple hardware interface for GPIO circuit; done, but not documented yet
* C# service to retrieve data from remote MongoDB instance and load into SQL database; not started

##Future goals
* Dashboard camera, possibly using a modified 808 keychain camera, remote controlled by the Pi or attached circuitry
* Hack my car and make it do fun things (because, really, why not?)
* [Maybe] add one or more laser rangefinders to gauge distance between my vehicle and vehicles around me
* Backup solar power and battery for when vehicle is off
* Visual feedback of vehicle performance
* Make it a media center, too
