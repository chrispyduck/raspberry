#!/bin/sh

# disable wireless power saving
echo "Enabling 802.11n adapter"
ip link set wlan0 up

# start audio daemon
echo "Starting bluetooth audio daemon"
sudo -u pi pulseaudio -D

# connect bluetooth devices
echo "Connecting to bluetooth device(s)"
bluetoothctl << EOF
power on
agent on
connect 2C:44:01:CF:73:FE
quit
EOF

# create virtual device for tethering
echo "Creating Bluetooth ethernet device"
dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_2C_44_01_CF_73_FE org.bluez.Network1.Connect string:'nap'

# start DHCP on that device
echo "Obtaining IP address from bluetooth master"
dhcpcd -t 0 bnep0 &

# play something to say we're all ready
echo "Playing startup sound"
FILE=`ls /home/pi/startup-sounds/*.wav | sort -R | head -n1`
amixer sset PCM 98%
aplay $FILE
amixer sset PCM 98%
