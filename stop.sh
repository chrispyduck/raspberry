#!/bin/sh

# deactivate USB devices
sudo sh -c `echo 0x0 > /sys/devices/platform/bcm2708_usb/buspower`
