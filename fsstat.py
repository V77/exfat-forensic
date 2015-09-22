#!/usr/bin/python

import sys
import struct
import os
from mbr3 import *




#---------Informations recherche dans VBR-------------------------
# exFAT VBR
#Taille de la VBR = 12 secteurs
#Signature emplacement [3:10]
#Cluster Heap Offset emplacement [88:92]
#Cluster Count emplacement [92:96]
#Root dir first cluster emplacement [96:100]
#partition offset emplacement [64:72]
#taille volume emplacement [72:80]
#Offset de la fat emplacement [80:84]
#taille de la fat emplacement [84:88]
#Volume serial number emplacement [100:104]
#Bytes per sector emplacement [108:109]
#sectors per cluster emplacement [109:110]
#nombre de fat emplacement [110:111]
#drive select emplacement [111:112]
#percent in use emplacement [112:113]
#reserved emplacement [113:120]
#bootcode emplacement [120:510]
#bootsignature emplacement [510:512]




#--------Fonction ffstat avec argument file1 (fichier dump a analyser)-------
def fsstat(file1):

	if ((sys.argv[2] == "-o")):
		partition = 0

		for p in partitions:
			if p.first_sector == int(sys.argv[3]):
				partition = p
				break

		if partition != 0:

			if partition.type == 0x07:
				dump = file1
				vbr_offset = int(sys.argv[3])
				vbr_offset = vbr_offset * 512
				dump.seek(vbr_offset)
				vbrcontent = dump.read(512)

				#------------Affiche Resultats-----------------
				print "FILE SYSTEM INFORMATION"
				print "------------------------------------------------"
				signature = vbrcontent[3:10]
				print "File System Type :",signature
				print " "
				#---on recupere la signature de la partition situe au 3eme jusqu au 10eme emplacement de notre variable vbrcontent

				print "METADATA INFORMATION"
				print "------------------------------------------------"
				cluster_heap_offset = struct.unpack("<I", vbrcontent[88:92])[0]
				print "Cluster Heap Offset : ", cluster_heap_offset
				#----on recupere l'offset du cluster et on le retourne (Little endian vers big endian) pour pouvoir l'afficher correctement

				cluster_count = struct.unpack("<I", vbrcontent[92:96])[0]
				print "Cluster Count : ",cluster_count

				root_dir_first_cluster = struct.unpack("<I", vbrcontent[96:100])[0]
				print "Root Dir First Cluster : ", root_dir_first_cluster

				print "CONTENT INFORMATION"
				print "------------------------------------------------"
				partition_offset=addr_vbr1 = struct.unpack("<Q", vbrcontent[64:72])[0]
				print "Partition Offset : ",partition_offset

				taille_vol = struct.unpack("<Q", vbrcontent[72:80])[0]
				print "Taille de la partition : ", taille_vol

				fat_offset = struct.unpack("<I", vbrcontent[80:84])[0]
				print "Fat Offset : ",fat_offset

				fat_size = struct.unpack("<I", vbrcontent[84:88])[0]
				print "Taille de la FAT : ", fat_size

				volume_serial_number = struct.unpack("<I", vbrcontent[100:104])[0]
				print "Volume Serial Number : ", volume_serial_number

				file_system_revision = struct.unpack("<H", vbrcontent[104:106])[0]
				print "File System Revision : ",file_system_revision

				volume_flags = struct.unpack("<H", vbrcontent[106:108])[0]
				print "Volume Flags : ",volume_flags

				bytes_per_sector = struct.unpack("<B", vbrcontent[108:109])[0]
				print "Bytes per sector : ",bytes_per_sector

				sectors_per_cluster = struct.unpack("<B", vbrcontent[109:110])[0]
				print "Sectors per Cluster : ", sectors_per_cluster

				number_of_fats = struct.unpack("<B", vbrcontent[110:111])[0]
				print "Number of fats : ",number_of_fats

				drive_select = struct.unpack("<B", vbrcontent[111:112])[0]
				print "Drive select : ", drive_select

				percent_in_use = struct.unpack("<B", vbrcontent[112:113])[0]
				print "Percent in use : ",percent_in_use

				reserved = vbrcontent[113:120]
				print "Reserved : ", reserved

				print "------------------------------------------------"
				boot_code = vbrcontent[120:510]
				print "Boot Code : ", boot_code

				boot_signature = struct.unpack("<H", vbrcontent[510:512])[0]
				print "Boot Signature : ",boot_signature
			else:
				print "Invalid Offset"
				exit(1)
		else:
			print "invalid IMAGE"
			exit(1)

	else:
		print "invalid argument"
		exit(1)