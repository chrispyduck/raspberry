#!/bin/sh

# disable wireless power saving 
echo "Disabling 802.11n adapter"
systemctl stop netctl-auto@wlan0

# disconnect and disable bluetooth
echo "Disconnecting and disabling bluetooth devices"
bluetoothctl << EOF
disconnect 2C:44:01:CF:73:FE
agent off
power off
quit
EOF

# close pulseaudio
echo "Closing bluetooth audio daemon"
killall pulseaudio

# close DHCP client
echo "Closing DHCP clients"
killall -q dhcpcd

# disable USB power
echo "Disabling USB power"
echo 0x0 > /sys/devices/platform/bcm2708_usb/buspower
