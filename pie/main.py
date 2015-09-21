#!/usr/bin/env python

from Mbr import *
from Exfat import *

def show_files(files, init_tab=0):
	for f in files:
		# If f is a dir
		if isinstance(f, list):
			show_files(f, init_tab+1)
		else:
			print "\t"*init_tab + f

if __name__ == "__main__":

	img = open('/home/pie/school/afti/forensic/project/exfat-forensic/exfat4/sandisk4.001', 'r').read()
	# img = open('/home/pie/school/afti/forensic/project/exfat-forensic/disk1.001', 'r').read()

	# MBR #
	mbr = Mbr(img[0:512])
	if not mbr.is_valid():
		print "[!] Invalid MBR. Exiting..."
		exit(1)

	for partition in mbr.partition_table.partitions:
		if partition.type == 0x7:
			print "[*] Found NTFS/exFAT partition in MBR"
			partition_start_offset = partition.first_sector*512
			partition_end_offset = partition_start_offset + (partition.size_in_sector*512)

			exfat = Exfat(img[partition_start_offset:partition_end_offset])

			show_files(exfat.list_files())
