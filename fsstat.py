#!/usr/bin/python

import sys
import struct
import os



def fsstat(file1):

#------------Ouverture Dump----------
	dump = file1
	vbr_offset = 0x00006600
	dump.seek(vbr_offset)
	vbrcontent = dump.read(512)

#-----------------Informations recerche dans VBR-------------------------
# exFAT VBR
#Taille de la VBR = 12 secteurs
#0:2 Jmp Instruction
#3:10 Signature exFAT
#65:72 adresse VBR1 = sector number 0x33	debut disque = 0x33*512 = 0x6600
#73:80 	Taille total du volume 
#81:84	Addresse de la fat
#85:88  taille de la fat
#89:92  data cluster region adresse
#93:96  number of cluster numer in the cluster heap
#97:100 cluster adresse of root dir 
#101:104 volume S/n
#105:106 exfat version
#107:108 flags
#109 bytes per sector
#110 sectors per cluster
#end of bootcode
#130 debut disque 



#------------Affiche Resultats-----------------
	print "FILE SYSTEM INFORMATION"
	print "------------------------------------------------"
	signature = vbrcontent[3:10]
	print "File System Type :",signature
	print " "


	print "METADATA INFORMATION"
	print "------------------------------------------------"
	cluster_heap_offset = struct.unpack("<I", vbrcontent[88:92])[0]
	print "Cluster Heap Offset : ", cluster_heap_offset

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