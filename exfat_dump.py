#!/usr/bin/python

import sys
import struct
import os


#!!!!!!!!!!!!!!!! Attention !!!!!!!!!!!!!!#
# Nommer vos fichiers en fonction des arguments declarees ci-dessous


#Ajoutez vos codes :

from mbr import *
from fsstat import *
from icat import *
from fls import *

#========================================================#
#	             Verification arguments					 #
#========================================================#

if len(sys.argv) < 2:
	print("Precisez une action en parametre")
	sys.exit(1)

if len(sys.argv) < 3:
	print("Precisez un fichier a analyser")
	sys.exit(1)

#========================================================#
#	               Chargement fichier					 #
#========================================================#


# Choix de l'option (case), si aucun choix ne match --> ERROR
if sys.argv[1] == 'mmls':
	#Ouverture du fichier appele par l'argument
	#python exfat_dump.py mmls ./exfat6/exfat6.001
	filename = sys.argv[2]
	d=open(filename, 'rb')
	image = d.read()
	init_part(image[0:512])
	mmls()
	d.close()
elif sys.argv[1] == 'fsstat':
	#Ouverture du fichier appele par l'argument
	# python exfat_dump.py fsstat -o 39 ./exfat6/exfat6.001
	filename = sys.argv[4]
	d=open(filename, 'rb')
	image = d.read()
	init_part(image[0:512])
	fsstat(d, partitions)
	d.close()
elif sys.argv[1] == 'fls':
	print 'fls'
	argc = len(sys.argv)
	if(argc != 4):
		print "python exfat_dump.py fls (-all|-root) ./exfat6/exfat6.001"
		exit(1)
	flag = sys.argv[2]
	filename = sys.argv[3]
	if flag == "-root":
		d=open(filename, 'rb')
		image = d.read()
		init_part(image[0:512])
		fls_root(image, partitions)
		d.close()
	elif flag == "-all":
		d=open(filename, 'rb')
		image = d.read()
		init_part(image[0:512])
		fls_filesystem(image, partitions)
		d.close()
elif sys.argv[1] == 'istat':
	print 'istat'
	d.close()
elif sys.argv[1] == 'icat':
	argc = len(sys.argv)
	if(argc < 6):
		print "Arguments missing"
		print "python exfat_dump.py icat -o 39 exfat6/exfat6.001 8 > tmp.pdf"
		exit(1)
	filename = sys.argv[4]
	d=open(filename, 'rb')
	image = d.read()
	init_part(image[0:512])
	icat(image)
	d.close()
else:
	print "ERROR : Entrez une option valide !"
	sys.exit(1)
