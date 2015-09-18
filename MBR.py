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


boot = content[0:440]
sig = content[441:446]
part_table = content[446:510]
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
	print ""
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
part_1 = part_table[16:32]
part_2 = part_table[32:48]
part_3 = part_table[48:64]

partitions=[]
partitions.append(part_0)
partitions.append(part_1)
partitions.append(part_2)
partitions.append(part_3)

type_part_dict = {'\x00':'NULL','\x01':'FAT12','\x0E':'FAT16','\x0B':'FAT32','\x0F':'Extended','\x05':'Extended','\x07':'NTFS','\x83':'Linux native','\x82':'Linux swap','\xEE':'EFI'}

j=0


for i in partitions:
	print "#=============================================================================#"
	print "#                               Partition "+str(j)+ "                                   #"
	print "#=============================================================================#"
	
	#def strcu partition
	boot_part = i[0]
	type_part = i[4]
	first_sect_part = i[8:12]
	nb_sect_part = i[12:16]

#========================================================#
#	            Verification type partition				 #
#========================================================#

#verif si type = 7 :
	
	print "Type Partition : "+type_part_dict[type_part]
	#print type_part



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
	j=j+1


print "#=============================================================================#"
print "#                                      Fin                                    #"
print "#=============================================================================#"

 


d.close()

