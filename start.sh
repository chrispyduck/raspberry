#!/bin/sh

# re-enable USB devices
echo 0x1 > /sys/devices/platform/bcm2708_usb/buspower

# start wireless networking
systemctl start netctl-auto@wlan0

# start audio daemon
echo "Starting bluetooth audio daemon"
mkdir /var/run/pulse
chown pulse:lp /var/run/pulse
sudo -u pulse pulseaudio -D --start
sleep 1

# connect bluetooth devices
echo "Connecting to bluetooth device(s)"
bluetoothctl << EOF
power on
agent on
default-agent
connect 2C:44:01:CF:73:FE
quit
EOF
sleep 1

# create virtual device for tethering
echo "Creating Bluetooth ethernet device"
dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_2C_44_01_CF_73_FE org.bluez.Network1.Connect string:'nap'
sleep 1

# start DHCP on that device
echo "Obtaining IP address from bluetooth master"
dhcpcd -t 0 bnep0 &

# play something to say we're all ready
#echo "Playing startup sound"
#FILE=`ls /home/pi/startup-sounds/*.wav | sort -R | head -n1`
#amixer sset PCM 98%
#aplay $FILE
#amixer sset PCM 98%
