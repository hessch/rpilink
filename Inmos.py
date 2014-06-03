#!/usr/bin/env python

import smbus

# data bus PCF8574 address
DATABUS_I2C_ADDR = 0x20

# control PCF8574 address
CONTROL_I2C_ADDR = 0x21

i2c = smbus.SMBus(0)

class c011:
	# ctrl maps c011 control signals to PCF8574 bits
	ctrl = [
		'RS0', 'RS1', 'RnotW'
	]

	def reset():
		"""Reset the C011 link adapter"""
	
		# make databus high for input
		i2c.write_byte(DATABUS_I2C_ADDR, 0xff)
	
	def write_byte(data):
		"""write data to the link"""
		
	
	def read_byte():
		"""read a byte from link"""
		
		return data
	
	def link_ready():
		"""test if link is ready (i.e. output buffer empty)"""
		
		return status

