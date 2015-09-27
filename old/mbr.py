#!/usr/bin/python

import sys
import struct
import os

class Partition(object):

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

	def __init__(self, payload):
		self.bootable = struct.unpack("<B", payload[0:1])[0]
		self.starting_chs = payload[1:4]
		self.type = struct.unpack("<B", payload[4:5])[0]
		self.ending_chs = payload[5:8]
	#========================================================#
	#	           		Analyse @ secteur 					 #
	#========================================================#
	# !!!!!!! Attention little endian !!!!!!!

		# struct.unpack --> "<" pour little endian
		self.first_sector = struct.unpack("<I", payload[8:12])[0]
		self.size_in_sector = struct.unpack("<I", payload[12:16])[0]

	def __repr__(self):
		return 	"\n\t\tbootable : " + str(hex(self.bootable)) + "\n" +\
				"\t\tstarting_chs : " + str(self.starting_chs) + "\n" +\
				"\t\ttype : " + str(hex(self.type)) + "\n" +\
				"\t\tending_chs : " + str(self.ending_chs) + "\n" +\
				"\t\tfirst_sector : " + str(hex(self.first_sector)) + "\n" +\
				"\t\tsize_in_sector : " + str(hex(self.size_in_sector)) + "\n"


# Tableau partition physique
partitions=[]

# Initialisation de la partition, appeler par tous les autres programmes
def init_part(content):
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
		sig = content[441:444]
		part_table = content[446:510]
		fin_mbr = content[510:512]


		#========================================================#
		#	              Verification de la MBR				 #
		#========================================================#


		# END OF MBR
		if fin_mbr == '\x55\xaa':


			# Definition structure table des partition + ajout dans le tebleau des partitions
			partitions.append(Partition(part_table[0:16]))
			partitions.append(Partition(part_table[16:32]))
			partitions.append(Partition(part_table[32:48]))
			partitions.append(Partition(part_table[48:64]))


		# Si fin des 512 bites != a 55aa :
		else:
			print "ERROR : MBR na pas ete trouve !"
			sys.exit(1)

def mmls():

		# Dictionnaire type de partition
		type_dict = {
			0x00 :'EMPTY',
			0x01 :'FAT12',
			0x04 :'FAT16',
			0x05 :'MS_EXTENTED',
			0x06 :'FAT16',
			0x07 :'NTFS', # 0x07 aussi EXFAT
			0x0B :'FAT32',
			0x0C :'FAT32',
			0x0E :'FAT16',
			0x0F :'MS_EXTENTED',
			0x11 :'HIDDEN_FAT12',
			0x14 :'HIDDEN_FAT16',
			0x16 :'HIDDEN_FAT16',
			0x1B :'HIDDEN_FAT32',
			0x1C :'HIDDEN_FAT32',
			0x1E :'HIDDEN_FAT16',
			0x42 :'MS_MBR_DYNAMIC',
			0x82 :'SOLARIS_X86',
			0x82 :'LINUX_SWAP',
			0x83 :'LINUX',
			0x84 :'HIBERNATION',
			0x85 :'LINUX_EXTENDED',
			0x86 :'NTFS_VOLUME_SET',
			0x87 :'NTFS_VOLUME_SET_1',
			0xA0 :'HIBERNATION_1',
			0xA1 :'HIBERNATION_2',
			0xA5 :'FREEBSD',
			0xA6 :'OPENBSD',
			0xA8 :'MACOS',
			0xA9 :'NETBSD',
			0xAB :'MAC_OX_BOOT',
			0xB7 :'BSDI',
			0xB8 :'BSDI_SWAP',
			0xEE :'EFI_GPT_DISK',
			0xEF :'EFI_SYSTEM_PARTITION',
			0xFB :'VMWARE_FILE_SYSTEM',
			0xFC :'VMWARE_SWAP'
		}

		# Compteur partition
		j=0

		# En-tete tableau
		print "Part	Boot	Start		End		Length		Description"

		for partition in partitions:

			# Decommente pour voir hexa partition :
			#print i.encode("hex")

		#========================================================#
		#	           Verification partition boot				 #
		#========================================================#


			#print repr(bootable)
			if partition.bootable == 0x80:
				boot_part_res = "Yes"
			else:
				boot_part_res = "No"


		#========================================================#
		#	            Verification type partition				 #
		#========================================================#


			# Si non vide Alors
			if partition.type != 0x00:

				# struct.unpack --> "<" pour little endian
				end_sect_part = partition.size_in_sector + partition.first_sector - 1


				#Format resultat
				#     "Part         	Boot	     				Start										End											Length								Description"
				print str(j)+"	"+boot_part_res+"	{0:010d}".format(partition.first_sector)+"	{0:010d}".format(partition.size_in_sector)+"	{0:010d}".format(end_sect_part)+"	"+type_dict[partition.type]+" (0x"+str(partition.type)+")"

				j=j+1

			else:
				#Format resultat type partition NULL
				#	 "Part			  Boot			  Start				End			  Length				Description"
				print str(j)+"	"+boot_part_res+"	----------"+"	----------"+"	----------	"+type_dict[partition.type]
				j=j+1
