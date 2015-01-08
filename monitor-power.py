#!/usr/bin/python3

# Test interrupts.

import select, time, sys

gpio_base = '/sys/class/gpio/'
gpio_pin_prefix = 'gpio'
pin_vbatt = '13'
pin_vacc = '19'

def write_once(path, value):
    f = open(path, 'w')
    f.write(value)
    f.close()
    return

def close_pin(num):
    write_once(gpio_base + 'unexport', num)
    return

def open_read_pin(num):
    write_once(gpio_base + 'export', num)
    pin_path = gpio_base + 'gpio' + num
    write_once(pin_path + '/direction', 'in')
    write_once(pin_path + '/edge', 'both')
    file = open(pin_path + '/value', 'r')
    return file

class PowerState:
    "describes the power state of this device"
    def __init__(self):
        self.vBatt = -1
        self.vAcc = -1
        self.vBattLast = -1
        self.vAccLast = -1
    def __enter__(self):
        self.__f_vBatt = open_read_pin(pin_vbatt)
        self.__f_vAcc = open_read_pin(pin_vacc)
        self.__poll = select.poll()
        self.__poll.register(self.__f_vBatt, select.POLLPRI)
        self.__poll.register(self.__f_vAcc, select.POLLPRI)
        return self
    def __exit__(self, type, value, traceback):
        self.__poll.unregister(self.__f_vBatt)
        self.__f_vBatt.close()
        close_pin(pin_vbatt)
        self.__poll.unregister(self.__f_vAcc)
        self.__f_vAcc.close()
        close_pin(pin_vacc)
    def print(self):
        sys.stdout.write("vBatt: {}, vAcc: {}\n".format(self.vBatt, self.vAcc))
        return
    def update(self):
        self.__f_vBatt.seek(0)
        self.vBatt = self.__f_vBatt.read(1)
        self.__f_vAcc.seek(0)
        self.vAcc = self.__f_vAcc.read(1)
        return
    def wait_for_event(self):
        while 1:
            event = self.poll()
            if len(event) == 0:
                continue
            self.update()
            if (self.vBatt == self.vBattLast) and (self.vAcc == self.vAccLast):
                continue
            return self
    def poll(self):
        return self.__poll.poll(6000)

with PowerState() as state:
    state.print()
    state.update()
    state.print()

    while 1:
        state.wait_for_event()
        state.print()


#state_last = PowerState(f_batt.read(1), f_acc.read(1))
#t1 = time.time()
#sys.stdout.write('Initial pin value = {}\n'.format(repr(state_last)))
#while 1:
#    events = po.poll(6000)
#    t2 = time.time()
#    f.seek(0)
#    state_last = f.read(1)
#    if len(events) == 0:
#        sys.stdout.write('  timeout  delta = {:8.4f} seconds\n'.format(t2 - t1))
#    else:
#        sys.stdout.write('value = {}  delta ={:8.4f}\n'.format(state_last, t2 - t1))
#        t1 = t2
