#!/usr/bin/env python

from Mbr import *
from Exfat import *

def show_files(files, init_tab=0):
	for idx,f in enumerate(files):
		# If f is a dir
		if isinstance(f, list):
			show_files(f, init_tab+1)
		else:
			print "\t"*init_tab + f

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
			print "[*] Found NTFS/exFAT partition in MBR\n"
			partition_start_offset = partition.first_sector*512
			partition_end_offset = partition_start_offset + (partition.size_in_sector*512)

			exfat = Exfat(img[partition_start_offset:partition_end_offset])

			print "v/v $MBR offset: 0x0  length: 512"
			print "v/v $VBR offset: " + str(hex(partition.first_sector*2**exfat.vbr.bytes_per_sector)) + "  length: " + str(2**exfat.vbr.bytes_per_sector)
			print "v/v $FAT offset: " + str(hex((exfat.vbr.fat_offset + partition.first_sector)*2**exfat.vbr.bytes_per_sector)) + "  length: " + str(hex(exfat.vbr.fat_length))
			print "r/r 3: " + exfat.root_dir.entries[0].entry.volume_label + " (Volume Label Directory Entry)"
			show_files(exfat.list_files())
			show_files(exfat.list_deleted_files())

	img_file.close()