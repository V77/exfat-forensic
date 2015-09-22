#!/usr/bin/python

from entry_types import *
from Vbr import *
import sys
import binascii
import math

#Gestion arguments
if len(sys.argv) < 4:
	print "Usage : list_files_rootdir.py -o [nbr first sector] [PATH]"
	sys.exit(1)
if sys.argv[1] != "-o":
	print "Usage : list_files_rootdir.py -o [nbr first sector] [PATH]"
	sys.exit(1)
try :
	int(sys.argv[2])
except :
	print "Usage : list_files_rootdir.py -o [nbr first sector] [PATH]"
	sys.exit(1)

#Ouverture fichier
filename = sys.argv[3]
d=open(filename, 'rb')
content = d.read(512)

#Offset VBR
first_sect_part=sys.argv[2]
offset_vbr=int(first_sect_part)*512
#print "Offset VBR : " + str(offset_vbr) 

#Offset rootdir
d.seek(0)
content = d.read()[offset_vbr:offset_vbr+512]
my_vbr=Vbr(content)
cluster_rootdir = my_vbr.root_dir_first_cluster
#print "Offset cluster RootDir : " + str(cluster_rootdir)

#Taille secteur
d.seek(0)
taille_sector=int(math.pow(2,my_vbr.bytes_per_sector))
#print "Taille secteur : " + str(taille_sector)

#Nombre de secteur par cluster
nbr_sector_per_cluster= int(math.pow(2,my_vbr.sectors_per_cluster))
#print "Nombre Secteur par Cluster : " + str(nbr_sector_per_cluster)

#Taille Cluster
taille_cluster=nbr_sector_per_cluster*taille_sector

#Offset Dataregion
data_region= offset_vbr+(256*512)
#print "Data region : " + str(data_region)

#Offset Rootdir
offset_rootdir = (cluster_rootdir-2)*taille_cluster + data_region
#print "Offset RootDir : " + str(offset_rootdir)

print "Type file\tOffset\t\t Name"

#Volume Label Entry
content = d.read()[offset_rootdir:offset_rootdir+taille_sector]
my_entry = Entry(content)
entry_type = my_entry.entry_type
if entry_type == VLDE:
	vlde_volume_label = my_entry.entry.volume_label
	print "/:\t\t" + str(offset_rootdir) + ":\t\t " + vlde_volume_label + " (Volume Label Entry)"


compteur = 0
d.seek(0)
offset_start= offset_rootdir
offset_end=offset_rootdir+32
flag=1

while flag!="00":

	content = d.read()[offset_start:offset_end]
	
	flag=binascii.b2a_hex(content[:1])
	#print flag

	if flag == "c1":
		start=2
		stop=32
		if type_file== "1000" :
			type_file = "d/d"
		elif type_file== "2000" :
			type_file = "r/r"
		print type_file + ":\t\t" + str(offset_start) + ":\t\t " + content[start:stop]
		type_file=="/"
	
	if flag == "85":
		type_file=str(binascii.b2a_hex(content[4:6]))
		 #print "Test file attributs : " + type_file

	if flag == "81":
		print  "/:\t\t" + str(offset_start) + ":\t\t $ALLOC_BITMAP"

	if flag == "82":
		print "/:\t\t" +str(offset_start) + ":\t\t $UPCASE_TABLE"

	d.seek(0)
	offset_start=offset_start+32
	offset_end=offset_end+32
	
	compteur=compteur+1
	#print compteur

print "/:\t\t0:\t\t $MBR"
offset_fat=65536 * taille_sector + offset_vbr
print "/:\t\t" + str(offset_fat) +":\t $FAT1" 

