#!/usr/bin/python

import sys
import struct
import os




filename = '/root/AFTI/disk1.001'
d=open(filename, 'rb')
content = d.read()[0:512]



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
	
boot = content[:439]
sig = content[440:444]
part_table = content[445:509]
fin_mbr = content[510:512]


	#------+------------------------+----------------+
	# HEX  |       DESC             | Size en Octets |
	#------+------------------------+----------------+
	# 01BE | Bootable (oui = 0x80)  |		1		 |
	#------+------------------------+----------------+
	# 01BF | obsolete				|		3		 |
	#------+------------------------+----------------+
	# 01C2 |Type Part, 7 = exFAT    |		1		 |
	#------+------------------------+----------------+
	# 01C3 | obsolete				|		3		 |
	#------+------------------------+----------------+
	# 01C6 | @ 1er secteur part		|		4		 |
	#------+------------------------+----------------+
	# 01CA | nb secteur dans part   |		4		 |
	#------+------------------------+----------------+
	# Total|						|	  16 (x4)	 |
	#------+------------------------+----------------+

#def struct table_part
part_1 = part_table[:15]
part_2 = part_table[16:31]
part_3 = part_table[32:47]
part_4 = part_table[48:]


#def strcu partition
type_part = part_1[:1]
boot_part = part_1[6]
first_sect_part = part_1[11:14]
nb_sect_part = part_1[12:16]

	
#========================================================#
#	                 Methode de lecture					 #
#========================================================#

#lire 1 byte = B
#---------------------------------------------
def read_1(content):
	return struct.unpack('B', content[0])[0]

#lire 2 byte = H
#---------------------------------------------
def read_2(content):
	return struct.unpack('H', content[0])[0]

#lire 4 byte = I
#---------------------------------------------
def read_4(content):
	return struct.unpack('I', content[0])[0]

#vérif si type = 7

#vérif si partition bootable

#calculer taille 


d.close()

