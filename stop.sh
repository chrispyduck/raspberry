#!/bin/sh

# disable wireless power saving 
echo "Disabling 802.11n adapter"
ip link set wlan0 down

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
sudo -u pi pulseaudio --kill

# close DHCP client
echo "Closing DHCP clients"
killall -q dhcpcd
