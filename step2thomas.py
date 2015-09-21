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
	print "Signature de la partition / Exemple : EXFAT"
	print "---------------------------------------------------------------FIND :           ", signature

def get_addr_vbr1():
	addr_vbr1 = vbrcontent[64:72]
	#print "test" , addr_vbr1
	print "Addresse de la VBR1 / exemple : 0x33"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[64:65].encode("hex")
	#print "Sector Address", struct.unpack('<Q', addr_vbr1)

def get_taille_vol():
	taille_vol = vbrcontent[72:80]
	print "Size of Total volume in sectors / Exemple : 0xED4D = 32mo"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[72:74].encode("hex")
	#print "Size of Total volume in sectors" ,struct.unpack('<Q', taille_vol)

def get_addr_fat1():
	addr_fat1 = vbrcontent[80:83]
	print "Addresse de la premiere FAT / Exemple Secteur 0x80 (+VBR)"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[80:81].encode("hex")
	#print "Addresse de la premiere FAT", struct.unpack('<I', addr_fat1)

def get_fat_size():
	fat_size = vbrcontent[84:100]
	print "Taille de la FAT / Exemple 0x40 sectors"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[84:85].encode("hex")
	#print struct.unpack('<I', fat_size)

def get_addr_data_region():
	addr_data_region = vbrcontent[88:91]
	print "Data / Cluster region address / Exemple 0x100 (+VBR)"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[89:91].encode("hex")
	#print struct.unpack('<I', addr_data_region)

def get_cluster_num():
	cluster_num = vbrcontent[92:96]
	print "Number of Cluster number in the cluster heap"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[92:94].encode("hex")
	#print struct.unpack('<I', cluster_num)

def get_bytes_per_sector():
	bytes_per_sector = vbrcontent[108]
	print "Bytes par secteur / Exemple 9 (2^9 = 512bytes)"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[108].encode("hex")
	#print struct.unpack('<I', bytes_per_sector)


def get_sect_per_cluster():
	bytes_per_cluster = vbrcontent[109]
	print "Secteurs par cluster / Exemple 3 (2^3 = 8)"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[109].encode("hex")
	#print struct.unpack('<I', bytes_per_sector)

def get_root_cluster():
	root_cluster = vbrcontent[97:100]
	print "Cluster adrress of root dir / Exemple 5"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[96:97].encode("hex")
	#print struct.unpack('<I', root_cluster)

def get_serial_num():
	serial_num = vbrcontent[106:107]
	print "Volume S/N"
	print "---------------------------------------------------------------FIND :           ",vbrcontent[100:104].encode("hex")
	#print struct.unpack('<I', serial_num)

#------------Affiche Resultats-----------------
print "Taille de la VBR: 12 sectors"
print "----------------------------"
get_signature()
get_addr_vbr1()
get_taille_vol()
get_addr_fat1()
get_fat_size()
get_addr_data_region()
get_cluster_num()
get_bytes_per_sector()
get_sect_per_cluster()
get_root_cluster()
get_serial_num()
