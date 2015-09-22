#!/usr/bin/python

import sys
import struct
import os


#!!!!!!!!!!!!!!!! Attention !!!!!!!!!!!!!!#
# Nommer vos fichiers en fonction des arguments declarees ci-dessous


#Ajoutez vos codes :
from mbr3 import *
from fsstat import *


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

#Ouverture du fichier appeler par l'argument
filename = sys.argv[2]
d=open(filename, 'rb')
init_part(d.read()[0:512])
# Choix de l'option (case), si aucun choix ne match --> ERROR
if sys.argv[1] == 'mmls':
	mmls()
	d.close()
elif sys.argv[1] == 'fsstat':
	fsstat(d)
	d.close()
elif sys.argv[1] == 'fls':
	print 'fls'
	d.close()
elif sys.argv[1] == 'istat':
	print 'istat'
	d.close()
elif sys.argv[1] == 'icat':
	print 'icat'
	d.close()
else:
	print "ERROR : Entrez une option valide !"
	d.close()
	sys.exit(1)
