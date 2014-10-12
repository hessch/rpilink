#!/usr/bin/env python 
"""
	simple test for Inmos link adapter
	Hessel Schut, hessel@isquared.nl, 2014-08-19
"""

import Inmos2

# create link instance on default addresses
link = Inmos2.Link()

# send data to link
while (1):
	for i in range(0xff):
		link.write(i)

		print ', '.join([
			'write: %02x' % i,
			'read: %02x' % link.read(),
		])
