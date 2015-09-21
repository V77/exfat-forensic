# Use in your code:
#
# from entry_types import *
# my_entry = Entry(raw_32_bytes_entry)
# entry_type = my_entry.entry_type
# if entry_type == VLDE:
# 	vlde_volume_label = my_entry.entry.volume_label
#
# This will automatically set the entry type depending on the raw_32_bytes_entry first byte,
# and create/fill the 'entry' object's attributes (depending on entry type)

import struct

# ENTRY TYPES #
VLDE 	= 0x83		# Volume Label Directory Entry
ABDE 	= 0x81		# Allocation Bitmap Directory Entry
UPCTDE 	= 0x82		# UP-Case Table Directory Entry
FDE 	= 0x85		# File Directory Entry
SEDE 	= 0xC0		# Stream Extension Directory Entry
FNEDE 	= 0xC1		# File Name Extension Directory Entry
VGDE 	= 0xA0		# Volume GUID Directory Entry
TFPDE	= 0xA1		# TexFAT Padding Directory Entry (TODO)
WCACTDE	= 0xE2		# Windows CE Access Control Table Directory Entry (TODO)

DELETED_FILE = 0x40

class Vlde(object):
	def __init__(self, payload):
		self.character_count = struct.unpack("<B", payload[1])[0]
		self.volume_label = payload[2:24]
		self.reserved = payload[24:32]

	def __repr__(self):
		return 	"Volume Label Directory Entry\n" +\
				"character_count : " + str(self.character_count) + "\n" +\
				"volume_label : " + str(self.volume_label) + "\n" +\
				"reserved : " + str(self.reserved) + "\n\n"

class Abde(object):
	def __init__(self, payload):
		self.bitmap_flags = struct.unpack("<B", payload[1])[0]
		self.reserved = payload[2:20]
		self.first_cluster = struct.unpack("<I", payload[20:24])[0]
		self.data_length = struct.unpack("<Q", payload[24:32])[0]

	def __repr__(self):
		return 	"Allocation Bitmap Directory Entry\n" +\
				"bitmap_flags : " + str(self.bitmap_flags) + "\n" +\
				"reserved : " + str(self.reserved) + "\n" +\
				"first_cluster : " + str(self.first_cluster) + "\n" +\
				"data_length : " + str(self.data_length) + "\n\n"

class Upctde(object):
	def __init__(self, payload):
		self.reserved1 = payload[1:4]
		self.table_checksum = struct.unpack("<I", payload[4:8])[0]
		self.reserved2 = payload[8:20]
		self.first_cluster = struct.unpack("<I", payload[20:24])[0]
		self.data_length = struct.unpack("<Q", payload[24:32])[0]

	def __repr__(self):
		return 	"UP-Case Table Directory Entry\n" +\
				"reserved1 : " + str(self.reserved1) + "\n" +\
				"table_checksum : " + str(self.table_checksum) + "\n" +\
				"reserved2 : " + str(self.reserved2) + "\n" +\
				"first_cluster : " + str(self.first_cluster) + "\n" +\
				"data_length : " + str(self.data_length) + "\n\n"

class Vgde(object):
	def __init__(self, payload):
		self.secondary_count = struct.unpack("<B", payload[1])[0]
		self.set_checksum = struct.unpack("<H", payload[2:4])[0]
		self.general_primary_flags = struct.unpack("<H", payload[4:6])[0]
		# self.volume_guid = struct.unpack("<")
		self.reserved = payload[22:32]

	def __repr__(self):
		return 	"Volume GUID Directory Entry\n" +\
				"secondary_count : " + str(self.secondary_count) + "\n" +\
				"set_checksum : " + str(self.set_checksum) + "\n" +\
				"general_primary_flags : " + str(self.general_primary_flags) + "\n" +\
				"reserved : " + str(self.reserved) + "\n\n"

class Fde(object):
	def __init__(self, payload):
		# exFAT Reverse Engineering Document Fields
		self.secondary_count = struct.unpack("<B", payload[1:2])[0]
		self.set_checksum = struct.unpack("<H", payload[2:4])[0]
		self.file_attributes = struct.unpack("<H", payload[4:6])[0]
		self.reserved1 = payload[6:8]
		self.create = struct.unpack("<I", payload[8:12])[0]
		self.last_modified = struct.unpack("<I", payload[12:16])[0]
		self.last_accessed = struct.unpack("<I", payload[16:20])[0]
		self.create_10ms = struct.unpack("<B", payload[20:21])[0]
		self.last_modified_10ms = struct.unpack("<B", payload[21:22])[0]
		self.create_tz_offset = struct.unpack("<B", payload[22:23])[0]
		self.last_modified_tz_offset = struct.unpack("<B", payload[23:24])[0]
		self.last_accessed_tz_offset = struct.unpack("<B", payload[24:25])[0]
		self.reserved2 = payload[25:32]

	def is_directory(self):
		attributes = "{0:016b}".format(self.file_attributes)[::-1]
		return True if int(attributes[4]) else False

	def __repr__(self):
		return 	"File Directory Entry\n" +\
				"secondary_count : " + str(self.secondary_count) + "\n" +\
				"set_checksum : " + str(self.set_checksum) + "\n" +\
				"file_attributes : " + "{0:016b}".format(self.file_attributes)[::-1] + "\n" +\
				"reserved1 : " + str(self.reserved1) + "\n" +\
				"create : " + str(self.create) + "\n" +\
				"last_modified : " + str(self.last_modified) + "\n" +\
				"last_accessed : " + str(self.last_accessed) + "\n" +\
				"create_10ms : " + str(self.create_10ms) + "\n" +\
				"last_modified_10ms : " + str(self.last_modified_10ms) + "\n" +\
				"create_tz_offset : " + str(self.create_tz_offset) + "\n" +\
				"last_modified_tz_offset : " + str(self.last_modified_tz_offset) + "\n" +\
				"last_accessed_tz_offset : " + str(self.last_accessed_tz_offset) + "\n" +\
				"reserved2 : " + str(self.reserved2) + "\n\n"

class Sede(object):
	def __init__(self, payload):
		self.general_secondary_flags = struct.unpack("<B", payload[1:2])[0]
		self.reserved1 = payload[2:3]
		self.name_length = struct.unpack("<B", payload[3:4])[0]
		self.name_hash = struct.unpack("<H", payload[4:6])[0]
		self.reserved2 = payload[6:8]
		self.valid_data_length = struct.unpack("<Q", payload[8:16])[0]
		self.reserved3 = payload[16:20]
		self.first_cluster = struct.unpack("<I", payload[20:24])[0]
		self.data_length = struct.unpack("<Q", payload[24:32])[0]

	def __repr__(self):
		return 	"Stream Extension Directory Entry\n" +\
				"general_secondary_flags : " + str(self.general_secondary_flags) + "\n" +\
				"reserved1 : " + str(self.reserved1) + "\n" +\
				"name_length : " + str(self.name_length) + "\n" +\
				"name_hash : " + str(self.name_hash) + "\n" +\
				"reserved2 : " + str(self.reserved2) + "\n" +\
				"valid_data_length : " + str(self.valid_data_length) + "\n" +\
				"reserved3 : " + str(self.reserved3) + "\n" +\
				"first_cluster : " + str(self.first_cluster) + "\n" +\
				"data_length : " + str(self.data_length) + "\n\n"

class Fnede(object):
	def __init__(self, payload):
		self.general_secondary_flags = struct.unpack("<B", payload[1:2])[0]
		self.file_name = payload[2:32]

	def __repr__(self):
		return 	"File Name Extension Directory Entry\n" +\
				"general_secondary_flags : " + str(self.general_secondary_flags) + "\n" +\
				"file_name : " + str(self.file_name) + "\n\n"

class Entry(object):
	def __init__(self, payload):

		self.entry_type = struct.unpack("<B", payload[0])[0]

		if self.entry_type == VLDE:
			self.entry = Vlde(payload)

		elif self.entry_type == ABDE:
			self.entry = Abde(payload)

		elif self.entry_type == UPCTDE:
			self.entry = Upctde(payload)

		elif self.entry_type == FDE:
			self.entry = Fde(payload)

		elif self.entry_type == SEDE:
			self.entry = Sede(payload)

		elif self.entry_type == FNEDE:
			self.entry = Fnede(payload)

		elif self.entry_type == VGDE:
			self.entry = Vgde(payload)

		else:
			# print "[!] Unknown entry type."
			self.entry = None

	def __repr__(self):
		if self.entry_type != 0x00 and self.entry_type != DELETED_FILE and self.entry_type != 0x41 and self.entry_type != 0x05:
			return "(" + str(hex(self.entry_type)) + ") " + self.entry.__repr__()