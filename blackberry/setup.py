#!/usr/bin/env python

import setuptools 

setuptools.setup(
    name='blackberry',
    version='0.1',
    description='Raspberry Pi Vehicle Black Box',
    author='chrispyduck',
    author_email='chrispyduck@no.ema.il',
    url='https://github.com/chrispyduck/raspberry',
    packages=['blackberry', 'blackberry.components', 'blackberry.configuration', 'blackberry.data', 'blackberry.shared', 'blackberry.tests'],
    package_dir={'blackberry': 'src/blackberry'},
    requires=['RPi.GPIO', 'pymongo', 'json', 'argparse', 'dbus', 'obd', 'psutil'],
    entry_points={
        'console_scripts': [
            'blackberry = blackberry.main:main'
        ]
    },
    test_suite='blackberry.tests'
 )