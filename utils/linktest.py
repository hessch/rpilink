#!/usr/bin/env python 
"""
	simple test for Inmos link adapter
	Hessel Schut, hessel@isquared.nl, 2014-08-19
"""

import Inmos
from time import sleep

# create link instance on default addresses
link = Inmos.Link(linkspeed = 20)

# send data to link
inb = 0x00
while True:
	for i in range(0xff):
		if link.data_present():
			inb = link.read()
		link.write(i)

		print ', '.join([
			'write: %02x' % i,
			'read: %02x' % inb,
		])
		sleep(0.025)
