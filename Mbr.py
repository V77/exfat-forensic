#!/usr/bin/env python

import struct

class Mbr(object):

	def __init__(self, payload):
		self.routine = payload[0:440]
		self.signature = struct.unpack("<I", payload[440:444])[0]
		self.null = payload[444:446]
		self.partition_table = PartitionTable(payload[446:510])
		self.boot_signature = struct.unpack("<H", payload[510:512])[0]

	def is_valid(self):
		return True if self.boot_signature == 0xAA55 else False

	def __repr__(self):
		return 	"routine : " + str(self.routine) + "\n" +\
				"signature : " + str(self.signature) + "\n" +\
				"null : " + str(self.null) + "\n" +\
				"partition_table : " + str(self.partition_table) + "\n" +\
				"boot_signature : " + str(hex(self.boot_signature)) + "\n"

class PartitionTable(object):

	def __init__(self, payload):
		self.partitions = [Partition(payload[0:16]), Partition(payload[16:32]), Partition(payload[32:48]), Partition(payload[48:64])]

	def __repr__(self):
		output = ""
		for idx, partition in enumerate(self.partitions):
			output = output + "\n\tpartition " + str(idx) + " : " + partition.__repr__()
		return output

class Partition(object):

	def __init__(self, payload):
		self.bootable = struct.unpack("<B", payload[0:1])[0]
		self.starting_chs = payload[1:4]
		self.type = struct.unpack("<B", payload[4:5])[0]
		self.ending_chs = payload[5:8]
		self.first_sector = struct.unpack("<I", payload[8:12])[0]
		self.size_in_sector = struct.unpack("<I", payload[12:16])[0]

	def __repr__(self):
		return 	"\n\t\tbootable : " + str(hex(self.bootable)) + "\n" +\
				"\t\tstarting_chs : " + str(self.starting_chs) + "\n" +\
				"\t\ttype : " + str(hex(self.type)) + "\n" +\
				"\t\tending_chs : " + str(self.ending_chs) + "\n" +\
				"\t\tfirst_sector : " + str(hex(self.first_sector)) + "\n" +\
				"\t\tsize_in_sector : " + str(hex(self.size_in_sector)) + "\n"


if __name__ == "__main__":

	f = open("../disk1.001")
	print Mbr(f.read(512))
	f.close()
