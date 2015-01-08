#!/bin/sh

# activate USB devices
#sudo sh -c `echo 0x1 > /sys/devices/platform/bcm2708_usb/buspower`
#sleep 1

# start audio daemon
pulseaudio -D

# connect bluetooth devices
bluetoothctl << EOF
power on
agent on
connect 2C:44:01:CF:73:FE
quit
EOF

# create virtual device for tethering
dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_2C_44_01_CF_73_FE org.bluez.Network1.Connect string:'nap'

# start DHCP on that device
sudo dhcpcd -t 0 eth0 &
sudo dhcpcd -t 0 bnep0 &

# play something to say we're all ready
FILE=`ls /home/pi/startup-sounds/*.wav | sort -R | head -n1`
amixer sset PCM 98%
aplay $FILE
amixer sset PCM 98%
