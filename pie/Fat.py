#!/usr/bin/env python

import struct

NO_SIGNIFICANT_MEANING = 0x00000000
NOT_A_VALID_CELL_VALUE = 0x00000001
LARGEST_VALUE = 0xFFFFFFF6
BAD_BLOCK = 0xFFFFFFF7
MEDIA_DESCRIPTOR = 0xFFFFFFF8
EOF = 0xFFFFFFFF

class Fat(object):

	def __init__(self, payload):
		n = 4						# 32 bits FAT cells
		# Split FAT in list of 4 bytes entries
		self.fat = [struct.unpack("<I", payload[i:i+n])[0] for i in range(0, len(payload), n)]

	def is_eof(self, cluster):
		return True if self.fat[cluster] == EOF else False

	def is_cluster_number(self, cluster):
		fat_entry = self.fat[cluster]
		return True if (fat_entry != NO_SIGNIFICANT_MEANING and fat_entry != NOT_A_VALID_CELL_VALUE and fat_entry != LARGEST_VALUE and fat_entry != BAD_BLOCK and fat_entry != MEDIA_DESCRIPTOR and fat_entry != EOF) else False

	def get_cluster_chain(self, cluster):
		if self.is_eof(cluster):
			return [cluster]
		elif self.is_cluster_number(cluster):
			return [cluster] + self.get_cluster_chain(self.fat[cluster])
		else:
			return []
