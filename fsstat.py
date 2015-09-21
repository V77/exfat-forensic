#!/usr/bin/python

import sys
import struct
import os


#------------Ouverture Dump----------
dump = open("disk1.001", "r")
vbr_offset = 0x00006600
dump.seek(vbr_offset)
vbrcontent = dump.read(512)

#print vbrcontent.encode("hex")


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

#--------------Fonctions Recuperation valeurs-------------	

def get_signature():
	signature = vbrcontent[3:10]
	print "File System Type :",signature

def get_addr_vbr1():
	addr_vbr1 = vbrcontent[64:65].encode("hex")
	print "Addresse de la VBR : ",vbrcontent[64:65].encode("hex")
	#print "Sector Address", struct.unpack('<2', addr_vbr1)

def get_partition_offset():
	partition_offset=addr_vbr1 = struct.unpack("<Q", vbrcontent[64:72])[0]
	print "Partition Offset : ",partition_offset

def get_taille_vol():
	taille_vol = struct.unpack("<Q", vbrcontent[72:80])[0]
	print "Taille de la partition : ", taille_vol

def get_fat_offset():
	fat_offset = struct.unpack("<I", vbrcontent[80:84])[0]
	print "Fat Offset : ",fat_offset

def get_fat_size():
	fat_size = struct.unpack("<I", vbrcontent[84:88])[0]
	print "Taille de la FAT : ", fat_size

def get_cluster_heap_offset():
	cluster_heap_offset = struct.unpack("<I", vbrcontent[88:92])[0]
	print "Cluster Heap Offset : ", cluster_heap_offset

def get_cluster_count():
	cluster_count = struct.unpack("<I", vbrcontent[92:96])[0]
	print "Cluster Count : ",cluster_count

def get_root_dir_first_cluster():
	root_dir_first_cluster = struct.unpack("<I", vbrcontent[96:100])[0]
	print "Root Dir First Cluster : ", root_dir_first_cluster

def get_volume_serial_number():
	volume_serial_number = struct.unpack("<I", vbrcontent[100:104])[0]
	print "Volume Serial Number : ", volume_serial_number

def get_file_system_revision():
	file_system_revision = struct.unpack("<H", vbrcontent[104:106])[0]
	print "File System Revision : ",file_system_revision

def get_volume_flags():
	volume_flags = struct.unpack("<H", vbrcontent[106:108])[0]
	print "Volume Flags : ",volume_flags

def get_bytes_per_sector():
	bytes_per_sector = struct.unpack("<B", vbrcontent[108:109])[0]
	print "Bytes per sector : ",bytes_per_sector

def get_sectors_per_cluster():
	sectors_per_cluster = struct.unpack("<B", vbrcontent[109:110])[0]
	print "Sectors per Cluster : ", sectors_per_cluster

def get_number_of_fats():
	number_of_fats = struct.unpack("<B", vbrcontent[110:111])[0]
	print "Number of fats : ",number_of_fats

def get_drive_select():
	drive_select = struct.unpack("<B", vbrcontent[111:112])[0]
	print "Drive select : ", drive_select

def get_percent_in_use():
	percent_in_use = struct.unpack("<B", vbrcontent[112:113])[0]
	print "Percent in use : ",percent_in_use

def get_reserved():
	reserved = vbrcontent[113:120]
	print "Reserved : ", reserved

def get_boot_code():
	boot_code = vbrcontent[120:510]
	print "Boot Code : ", boot_code

def get_boot_signature():
	boot_signature = struct.unpack("<H", vbrcontent[510:512])[0]
	print "Boot Signature : ",boot_signature


#------------Affiche Resultats-----------------
print "FILE SYSTEM INFORMATION"
print "------------------------------------------------"
get_signature()
print " "


print "METADATA INFORMATION"
print "------------------------------------------------"
get_cluster_heap_offset()
get_cluster_count()
get_root_dir_first_cluster()

print "CONTENT INFORMATION"
print "------------------------------------------------"
get_partition_offset()
get_taille_vol()
get_fat_offset()
get_fat_size()
get_volume_serial_number()
get_file_system_revision()
get_volume_flags()
get_bytes_per_sector()
get_sectors_per_cluster()
get_number_of_fats()
get_drive_select()
get_percent_in_use()
get_reserved()
print "------------------------------------------------"
get_boot_code()
get_boot_signature()



