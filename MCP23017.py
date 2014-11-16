#!/usr/bin/env python

# MCP23017 i2c gpio controller module
# Copyright (C) 2014 Hessel Schut, hessel@isquared.nl

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import smbus

# IOCON.BANK defaults to 0 (bytewise mode)

DEVICE_ADDRESS = 0x20 # Device address (A0-A2)

IODIRA = 0x00 # Port A direction register
IODIRB = 0x01 # Port B direction register
GPPUA  = 0x0c # Port A pull-up configuration register
GPPUB  = 0x0d # Port B pull-up configuration register

OLATA  = 0x14 # Port A output latch register
OLATB  = 0x15 # Port B output latch register
GPIOA  = 0x12 # Port A GPIO register
GPIOB  = 0x13 # Port B GPIO register

INPUT  = 0xff # shorthand for all pins as input
OUTPUT = 0x00 # shorthand for all pins as output


class gpio:
	def __init__(self, device_address = DEVICE_ADDRESS):
		"""Create MCP23017 instance."""
		if device_address is None:
			self.device_address = DEVICE_ADDRESS
		else:
			self.device_address = device_address

		self.i2cbus = smbus.SMBus(1)
		
	def write(self, register, data):
		"""Write `data` to register."""
		self.i2cbus.write_byte_data(
			self.device_address,
			register,
			data)

	def read(self, register):
		"""Read from register."""
		return self.i2cbus.read_byte_data(
			self.device_address,
			register)
