#!/usr/bin/env python

from Mbr import *
from Exfat import *

def show_files(files, parent=""):
	for idx,f in enumerate(files):
		# If f is a dir
		if isinstance(f, list):
			file_parent = files[idx-1].replace(' ', '').split('|')[0]
			show_files(f, "/" + file_parent)
		else:
			print parent + "/" + f

if __name__ == "__main__":

	img_file = open('/home/pie/school/afti/forensic/project/exfat-forensic/exfat4/sandisk4.001', 'r')
	# img_file = open('/home/pie/school/afti/forensic/project/exfat-forensic/disk1.001', 'r')
	img = img_file.read()

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
	img_file.close()