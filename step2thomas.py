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
	print "Signature de la partition :", signature

def get_addr_vbr1():

	addr_vbr1 = vbrcontent[64:72]
	print "Sector Address",vbrcontent[64:72].encode("hex")
	#print "Sector Address", struct.unpack('<Q', addr_vbr1)

def get_taille_vol():
	taille_vol = vbrcontent[72:80]
	print "Size of Total volume in sectors",vbrcontent[72:80].encode("hex")
	#print "Size of Total volume in sectors" ,struct.unpack('<Q', taille_vol)

def get_addr_fat1():
	addr_fat1 = vbrcontent[80:84]
	print "Addresse de la premiere FAT",vbrcontent[80:84].encode("hex")
	#print "Addresse de la premiere FAT", struct.unpack('<I', addr_fat1)

def get_fat_size():
	fat_size = vbrcontent[85:88]
	print "Taille de la FAT",vbrcontent[85:88].encode("hex")
	#print struct.unpack('<I', fat_size)

def get_addr_data_region():
	addr_data_region = vbrcontent[89:92]
	print "Addresse Data Region",vbrcontent[89:92].encode("hex")
	#print struct.unpack('<I', addr_data_region)

def get_cluster_num():
	cluster_num = vbrcontent[93:96]
	print "Nombre Cluster",vbrcontent[93:96].encode("hex")
	#print struct.unpack('<I', cluster_num)

def get_bytes_per_sector():
	bytes_per_sector = vbrcontent[109]
	print "Bytes par secteur",vbrcontent[109].encode("hex")
	#print struct.unpack('<I', bytes_per_sector)


def get_sect_per_cluster():
	bytes_per_cluster = vbrcontent[110]
	print "secteurs par cluster",vbrcontent[110].encode("hex")
	#print struct.unpack('<I', bytes_per_sector)

def get_root_cluster():
	root_cluster = vbrcontent[97:100]
	print "Cluster racine",vbrcontent[97:100].encode("hex")
	#print struct.unpack('<I', root_cluster)

def get_serial_num():
	serial_num = vbrcontent[101:104]
	print "numero de serie",vbrcontent[101:104].encode("hex")
	#print struct.unpack('<I', serial_num)

#------------Affiche Resultats-----------------
print "VBR size : 12 sectors"
get_signature()
get_addr_vbr1()
get_taille_vol()
get_addr_fat1()
get_fat_size()
get_addr_data_region()
get_cluster_num
get_bytes_per_sector
get_sect_per_cluster
get_root_cluster
get_serial_num
