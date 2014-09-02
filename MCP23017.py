#!/usr/bin/env python

# MCP23017 i2c gpio controller module
# Hessel Schut, hessel@isquared.nl, 2014-10-12

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


class gpio:
	def __init__(self, device_address = DEVICE_ADDRESS):
		'''Create MCP23017 instance.'''
		if device_address is None:
			self.device_address = DEVICE_ADDRESS
		else:
			self.device_address = device_address

		self.i2cbus = smbus.SMBus(1)
		
	def write(self, register, data):
		'''Write `data` to register.'''
		self.i2cbus.write_byte_data(
			self.device_address,
			register,
			data)

	def read(self, register):
		'''Read from register.'''
		return self.i2cbus.read_byte_data(
			self.device_address,
			register)
