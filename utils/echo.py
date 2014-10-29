#!/usr/bin/env python 
"""
	simple test for Inmos link adapter
	Hessel Schut, hessel@isquared.nl, 2014-08-19
"""

import Inmos

# create link instance on default addresses
link = Inmos.Link()

# send data to link
inb = 0x00
while True:
	if link.data_present():
		inb = link.read()
		while True:
			if link.output_ready():
				break
		link.write(inb)

