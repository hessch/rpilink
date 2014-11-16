#!/usr/bin/python

# tdetect.py - simple transputer detection program
#
# initial version: Hessel Schut, hessel@isquared.nl, 2013-12-25
#	for AVM PCMCIA ISDN adapters.
# 	Based on Linux capi/link drivers, ispy and Axel Muhr's T2C64 code.
#
# 2014-10-13: quick and very dirty rewrite to test C012 link 
#             with the new Inmos2 module

import sys, time
import Inmos

link = Inmos.Link(linkspeed=10)
link.enable_interrupts()

# write identification code to link
boot_code = [
	0xb1, 			# AJW 1
	0xd1, 			# STL 1
	0x24, 0xf2, 		# MINT
	0x21, 0xfc, 		# STHF
	0x24, 0xf2, 		# MINT
	0x21, 0xf8,		# STLF
	0xf0, 			# REV
	0x60, 0x5c, 		# LDNLP -4
	0x2a, 0x2a, 0x2a, 0x4a, # LDC #AAAA
	0xff, 			# OUTWORD
	0x21, 0x2f, 0xff, 	# START
	0x02, 0x00		# C004 read link
];

print 'Writing %d bytes of boot code to Transputer:' % len(boot_code)
i = 0
link.write(len(boot_code))
for byte in boot_code:
	if i % 16 == 0:
		sys.stdout.write("\n\t")
	sys.stdout.write("%02x " % byte)
	i += 1
	link.write(byte)

print; print

# wait for result
retries = 16 
while link.data_present() is False and retries > 0:
	time.sleep(0.01)
	retries -= 1
if retries <= 0:
	print
	print "Timeout waiting for result from Transputer"
	print
	exit()

# read result
print "Read result from Transputer:"
i = 0
while link.data_present():
	if i % 16 == 0:
		sys.stdout.write("\n\t")
	sys.stdout.write(('%02x ' % link.read()).zfill(2))
	i += 1
print ; print

# identify Transputer family
if i == 1:
	print 'IMSC004 link switch found'
elif i == 2:
	print '16-bit Transputer found'
elif i == 4:
	print '32-bit Transputer found'
else:
	print 'No Transputer found, got %d bytes back from link' % i
print
	
