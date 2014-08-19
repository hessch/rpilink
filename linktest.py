#!/usr/bin/env python 
"""
	simple test for Inmos link adapter
	Hessel Schut, hessel@isquared.nl, 2014-08-19
"""

import Inmos

# create link instance on default addresses
link = Inmos.c011()

# reset link
link.reset()

# send data to link
while (1):
	for i in range(255):
		# link.reset()
		link.write_byte(i)


		print ', '.join([
			'write: %02x' % i,
			'read: %02x' % link.read_byte(),
			'ostat: %d' % link.link_ready(),
			'istat: %d' % link.data_present()
		])
