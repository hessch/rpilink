#!/usr/bin/env python

import smbus

# data bus PCF8574 address
DATABUS_I2C_ADDR = 0x20

# control PCF8574 address
CONTROL_I2C_ADDR = 0x21

i2c = smbus.SMBus(1)

class c011:
	def __init__(self, dbus_addr=None, ctrl_addr=None):
		"""
		create Inmos Link, optionally specifying i2c addresses
		"""
		if dbus_addr is None:
			self.dbus_addr = DATABUS_I2C_ADDR
		else:
			self.dbus_addr = dbus_addr
		
		if ctrl_addr is None:
			self.ctrl_addr = CONTROL_I2C_ADDR
		else:
			self.ctrl_addr = ctrl_addr
		
	# ctrl maps c011 control signals to PCF8574 bits
	ctrl = [
		'LED0', 'LinkSpeed', 'LED1', 'Reset', 
		'RS0', 'RS1', 'RnotW', 'notCS'
	]

	def reset(self):
		"""Reset the C011 link adapter"""
		# assert reset
		i2c.write_byte(self.ctrl_addr, 
			1 << self.ctrl.index('Reset') |
			1 << self.ctrl.index('LED1'))
		# make databus high for input
		i2c.write_byte(self.dbus_addr, 0xff)
		# deassert reset, deassert notCS
		i2c.write_byte(self.ctrl_addr, 
			1 << self.ctrl.index('notCS'))
	
	def write_byte(self, data):
		"""write data to the link"""

		# setup regs for write
		i2c.write_byte(self.ctrl_addr, 
			1 << self.ctrl.index('RS0')   | 
			1 << self.ctrl.index('notCS') | 
			1 << self.ctrl.index('LED0'))

		# copy data to bus
		i2c.write_byte(self.dbus_addr, data)

		# assert notCS
		i2c.write_byte(self.ctrl_addr, 
			1 << self.ctrl.index('RS0') | 
			1 << self.ctrl.index('LED0'))

		# deassert notCS
		i2c.write_byte(self.ctrl_addr, 
			1 << self.ctrl.index('notCS'))
		
	def read_byte(self):
		"""read a byte from link"""

		# setup regs for read, notCS still deasserted
		i2c.write_byte(self.ctrl_addr, 
			1 << self.ctrl.index('RnotW') |
			1 << self.ctrl.index('notCS'))

		# setup databus for reading
		i2c.write_byte(self.dbus_addr, 0xff)

		# assert notCS		
		i2c.write_byte(self.ctrl_addr, 
			1 << self.ctrl.index('RnotW'))

		# read data byte
		data = i2c.read_byte(self.dbus_addr)

		# let go of notCS
		i2c.write_byte(self.ctrl_addr, 
			1 << self.ctrl.index('notCS'))

		# and return byte
		return data
	
	def link_ready(self):
		"""
		test if link is ready (i.e. output buffer empty)
		"""
		
		# setup regs for write, notCS still deasserted
		i2c.write_byte(self.ctrl_addr,
			1 << self.ctrl.index('RnotW') |
			1 << self.ctrl.index('RS0')   |
			1 << self.ctrl.index('RS1')   |
			1 << self.ctrl.index('notCS'))

		# setup databus for reading
		i2c.write_byte(self.dbus_addr, 0xff)
		
		# assert notCS
		i2c.write_byte(self.ctrl_addr,
			1 << self.ctrl.index('RnotW') |
			1 << self.ctrl.index('RS0')   |
			1 << self.ctrl.index('RS1'))

		# read status register, mask output ready bit
		status = i2c.read_byte(self.dbus_addr) & 0x01
	
		# let go of notCS
		i2c.write_byte(self.ctrl_addr,
			1 << self.ctrl.index('notCS'))
		
		return status

	def data_present(self):
		"""
		test if unread input data present on link interface
		"""
		
		# setup regs for write, notCS still deasserted
		i2c.write_byte(self.ctrl_addr,
			1 << self.ctrl.index('RnotW') |
			1 << self.ctrl.index('RS1')   |
			1 << self.ctrl.index('notCS'))

		# setup databus for reading
		i2c.write_byte(self.dbus_addr, 0xff)
		
		# assert notCS
		i2c.write_byte(self.ctrl_addr,
			1 << self.ctrl.index('RnotW') |
			1 << self.ctrl.index('RS1'))

		# read status register, mask data present  bit
		status = i2c.read_byte(self.dbus_addr) & 0x01
	
		# let go of notCS
		i2c.write_byte(self.ctrl_addr,
			1 << self.ctrl.index('notCS'))
		
		return status

