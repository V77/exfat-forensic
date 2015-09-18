#!/usr/bin/python

import sys
import struct
import os


#========================================================#
#	               Chargement fichier					 #
#========================================================#

filename = '/root/AFTI/disk1.001'
d=open(filename, 'rb')
content = d.read()[0:512]


	
#========================================================#
#	                 Methode de lecture					 #
#========================================================#

#lire 1 byte = B
#---------------------------------------------
def read_1(data):
	return struct.unpack('< B', data)

#lire 2 byte = H
#---------------------------------------------
def read_2(data):
	return struct.unpack('< H', data)

#lire 4 byte = I
#---------------------------------------------
def read_4(data):
	return struct.unpack('< I', data)


#========================================================#
#	           Initialisation Variable MBR				 #
#========================================================#


	#------+------------------------+----------------+
	# HEX  |       DESC             | Size en Octets |
	#------+------------------------+----------------+
	# 0000 | Routine de boot        |   	440		 |
	#------+------------------------+----------------+
	# 01B8 | Signature factultative |		 4       |
	#------+------------------------+----------------+
	# 01BC |           NULL         |		 2       |
	#------+------------------------+----------------+
	# 01BE | Table des partition    |		 64      |
	#------+------------------------+----------------+
	# 01FE |		FIN MBR			|		 2		 |
	#------+------------------------+----------------+
	# Total|						|	    512		 |
	#------+------------------------+----------------+ 


boot = content[:440]
sig = content[441:445]
part_table = content[446:509]
fin_mbr = content[510:512]



#========================================================#
#	              Verification de la MBR				 #
#========================================================#


#print len(content)
#print type(content)
#print content.encode("hex")

#print len(fin_mbr)
#print type(fin_mbr)
#print fin_mbr.encode("hex")

if fin_mbr == '\x55\xaa':
	print 'MBR OK'
else:
	print 'MBR NOK'


#========================================================#
#	            Initialisation Partitions				 #
#========================================================#


	#------+------------------------+----------------+
	# HEX  |       DESC             | Size en Octets |
	#------+------------------------+----------------+
	# 01BE | Bootable (oui = 0x80)  |		1	(0)	 |
	#------+------------------------+----------------+
	# 01BF | obsolete				|		3  (1-3) |
	#------+------------------------+----------------+
	# 01C2 |Type Part, 7 = exFAT    |		1	4	 |
	#------+------------------------+----------------+
	# 01C3 | obsolete				|		3	5-7	 |
	#------+------------------------+----------------+
	# 01C6 | @ 1er secteur part		|		4	8-11 |
	#------+------------------------+----------------+
	# 01CA | nb secteur dans part   |		4 12-15	 |
	#------+------------------------+----------------+
	# Total|						|	  16 (x4)	 |
	#------+------------------------+----------------+

#def struct table_part
part_0 = part_table[0:16]
part_1 = part_table[17:32]
part_2 = part_table[33:48]
part_3 = part_table[49:]

#print part_0.encode("hex")
#def strcu partition

boot_part = part_0[0]
type_part = part_0[4]
first_sect_part = part_0[8:12]
nb_sect_part = part_0[12:16]


#========================================================#
#	            Verification type partition				 #
#========================================================#


#verif si type = 7

type_part_dict = {'\x01':'FAT12','\x0E':'FAT16','\x0B':'FAT32','\x0F':'Extended','\x05':'Extended','\x07':'NTFS','\x83':'Linux native','\x82':'Linux swap','\xEE':'EFI'}

#print type_part
print "Type Partition : "+type_part_dict[type_part]


#========================================================#
#	           Verification partition boot				 #
#========================================================#

if boot_part == '\x80':
	print 'Partition bootable'
else:
	print 'Partition non bootable'
#print repr(boot_part)


#========================================================#
#	           		Analyse @ secteur 					 #
#========================================================#
# !!!!!!! Attention little endian !!!!!!!

first_sect_part = struct.unpack('<I',first_sect_part)[0]
nb_sect_part = struct.unpack('<I',nb_sect_part)[0]
end_sect_part = nb_sect_part + first_sect_part -1

print "Start = "+ str(first_sect_part)
print "Length = "+ str(nb_sect_part)
print "End = "+str(end_sect_part)

 


d.close()

