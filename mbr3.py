#!/usr/bin/python

import sys
import struct
import os

class Partition():

	def __init__(self,payload):

		self.boot_part = payload[0]
		self.type_part = payload[4]
		self.first_sect_part = payload[8:12]
		self.nb_sect_part = payload[12:16]


# Tableau partition physique
partitions=[]
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


		#print len(content)
		#print type(content)
		#print content.encode("hex")

		#print len(fin_mbr)
		#print type(fin_mbr)
		#print fin_mbr.encode("hex")

		# END OF MBR
		if fin_mbr == '\x55\xaa':

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

			# Definition structure table des partition
			partitions.append(Partition(part_table[0:16]))
			partitions.append(Partition(part_table[16:32]))
			partitions.append(Partition(part_table[32:48]))
			partitions.append(Partition(part_table[48:64]))


			for partition in partitions:

			#========================================================#
			#	            Verification type partition				 #
			#========================================================#


				# Si non vide Alors
				if partition.type_part != '\x00':


			#========================================================#
			#	           		Analyse @ secteur 					 #
			#========================================================#
			# !!!!!!! Attention little endian !!!!!!!

					# struct.unpack --> "<" pour little endian
					partition.first_sect_part = struct.unpack('<I',partition.first_sect_part)[0]
					partition.nb_sect_part = struct.unpack('<I',partition.nb_sect_part)[0]

		# Si fin des 512 bites != a 55aa :
		else:
			print "ERROR : MBR na pas ete trouve !"
			sys.exit(1)

def mmls():

		# Dictionnaire type de partition
		type_part_dict = {
			'\x00':'EMPTY',
			'\x01':'FAT12',
			'\x04':'FAT16',
			'\x05':'MS_EXTENTED',
			'\x06':'FAT16',
			'\x07':'NTFS', # 0x07 aussi EXFAT
			'\x0B':'FAT32',
			'\x0C':'FAT32',
			'\x0E':'FAT16',
			'\x0F':'MS_EXTENTED',
			'\x11':'HIDDEN_FAT12',
			'\x14':'HIDDEN_FAT16',
			'\x16':'HIDDEN_FAT16',
			'\x1B':'HIDDEN_FAT32',
			'\x1C':'HIDDEN_FAT32',
			'\x1E':'HIDDEN_FAT16',
			'\x42':'MS_MBR_DYNAMIC',
			'\x82':'SOLARIS_X86',
			'\x82':'LINUX_SWAP',
			'\x83':'LINUX',
			'\x84':'HIBERNATION',
			'\x85':'LINUX_EXTENDED',
			'\x86':'NTFS_VOLUME_SET',
			'\x87':'NTFS_VOLUME_SET_1',
			'\xA0':'HIBERNATION_1',
			'\xA1':'HIBERNATION_2',
			'\xA5':'FREEBSD',
			'\xA6':'OPENBSD',
			'\xA8':'MACOS',
			'\xA9':'NETBSD',
			'\xAB':'MAC_OX_BOOT',
			'\xB7':'BSDI',
			'\xB8':'BSDI_SWAP',
			'\xEE':'EFI_GPT_DISK',
			'\xEF':'EFI_SYSTEM_PARTITION',
			'\xFB':'VMWARE_FILE_SYSTEM',
			'\xFC':'VMWARE_SWAP'
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


			#print repr(boot_part)
			if partition.boot_part == "\x80":
				boot_part_res = "Yes"
			else:
				boot_part_res = "No"


		#========================================================#
		#	            Verification type partition				 #
		#========================================================#


			# Si non vide Alors
			if partition.type_part != '\x00':

			#print type_part_dict[type_part]
			#print type_part


		#========================================================#
		#	           		Analyse @ secteur 					 #
		#========================================================#
		# !!!!!!! Attention little endian !!!!!!!

				# struct.unpack --> "<" pour little endian
				end_sect_part = partition.nb_sect_part + partition.first_sect_part - 1


				#Format resultat
				print str(j)+"	"+boot_part_res+"	{0:010d}".format(partition.first_sect_part)+"	{0:010d}".format(partition.nb_sect_part)+"	{0:010d}".format(end_sect_part)+"	"+type_part_dict[partition.type_part]+" (0x"+partition.type_part.encode("hex")+")"

				j=j+1

			else:
				#Format resultat type partition NULL
				print str(j)+"	"+boot_part_res+"	----------"+"	----------"+"	----------	"+type_part_dict[partition.type_part]
				j=j+1
