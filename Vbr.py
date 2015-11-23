#!/usr/bin/env python

import struct

class Vbr(object):
	def __init__(self, payload):
		self.jmp_instruction = payload[0:3]
		self.file_system_name = payload[3:11]
		self.must_be_zero = payload[11:64]
		self.partition_offset = struct.unpack("<Q", payload[64:72])[0]
		self.volume_length = struct.unpack("<Q", payload[72:80])[0]
		self.fat_offset = struct.unpack("<I", payload[80:84])[0]
		self.fat_length = struct.unpack("<I", payload[84:88])[0]
		self.cluster_heap_offset = struct.unpack("<I", payload[88:92])[0]
		self.cluster_count = struct.unpack("<I", payload[92:96])[0]
		self.root_dir_first_cluster = struct.unpack("<I", payload[96:100])[0]
		self.volume_serial_number = struct.unpack("<I", payload[100:104])[0]
		self.file_system_revision = struct.unpack("<H", payload[104:106])[0]
		self.volume_flags = struct.unpack("<H", payload[106:108])[0]
		self.bytes_per_sector = struct.unpack("<B", payload[108:109])[0]		# In power of 2
		self.sectors_per_cluster = struct.unpack("<B", payload[109:110])[0]		# In power of 2
		self.number_of_fats = struct.unpack("<B", payload[110:111])[0]
		self.drive_select = struct.unpack("<B", payload[111:112])[0]
		self.percent_in_use = struct.unpack("<B", payload[112:113])[0]
		self.reserved = payload[113:120]
		self.boot_code = payload[120:510]
		self.boot_signature = struct.unpack("<H", payload[510:512])[0]

	def is_valid(self):
		return True if self.boot_signature == 0xAA55 else False

	def __repr__(self):
		return	"jmp_instruction : " + str(self.jmp_instruction) + "\n" +\
				"file_system_name : " + str(self.file_system_name) + "\n" +\
				"must_be_zero : " + str(self.must_be_zero) + "\n" +\
				"partition_offset : " + str(self.partition_offset) + "\n" +\
				"volume_length : " + str(self.volume_length) + "\n" +\
				"fat_offset : " + str(self.fat_offset) + "\n" +\
				"fat_length : " + str(self.fat_length) + "\n" +\
				"cluster_heap_offset : " + str(self.cluster_heap_offset) + "\n" +\
				"cluster_count : " + str(self.cluster_count) + "\n" +\
				"root_dir_first_cluster : " + str(self.root_dir_first_cluster) + "\n" +\
				"volume_serial_number : " + str(self.volume_serial_number) + "\n" +\
				"file_system_revision : " + str(self.file_system_revision) + "\n" +\
				"volume_flags : " + str(self.volume_flags) + "\n" +\
				"bytes_per_sector : " + str(self.bytes_per_sector) + "\n" +\
				"sectors_per_cluster : " + str(self.sectors_per_cluster) + "\n" +\
				"number_of_fats : " + str(self.number_of_fats) + "\n" +\
				"drive_select : " + str(self.drive_select) + "\n" +\
				"percent_in_use : " + str(self.percent_in_use) + "\n" +\
				"reserved : " + str(self.reserved) + "\n" +\
				"boot_code : " + str(self.boot_code) + "\n" +\
				"boot_signature : " + str(self.boot_signature) + "\n"


if __name__ == "__main__":

	f = open("./exfat1/disk1.001")
	f.seek(51*512)
	print Vbr(f.read(512))
	f.close()
