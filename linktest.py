#!/usr/bin/env python 

import Inmos

# create link instance on default addresses
link = Inmos.c011()

# reset link
link.reset()

# send data to link
while (1):
	for i in range(255):
		link.write_byte(i)

