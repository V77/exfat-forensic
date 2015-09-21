#!/usr/bin/env python

from Vbr import *
from entry_types import *
from Fat import *
from RootDir import *
from AllocationBitmap import *

CLUSTER_START = 2

class Exfat(object):

	def __init__(self, payload):
		self.payload = payload
		self.init_vbr()
		self.init_fat()
		self.init_root_dir()
		self.init_allocation_bitmap()

	def init_vbr(self):
		self.vbr = Vbr(self.payload[0:512])

	def init_fat(self):
		fat_addr = self.vbr.fat_offset * (2**self.vbr.bytes_per_sector)
		fat_size_in_bytes = self.vbr.fat_length*(2**self.vbr.bytes_per_sector)
		fat_raw = self.payload[fat_addr:fat_addr+fat_size_in_bytes]
		self.fat = Fat(fat_raw)

	def init_root_dir(self):
		root_dir_clusters = self.fat.get_cluster_chain(self.vbr.root_dir_first_cluster)
		root_dir_clusters_raw = self.get_clusters(root_dir_clusters)
		root_dir_entries = self.get_entries(root_dir_clusters_raw)
		self.root_dir = RootDir(root_dir_entries)

	def init_allocation_bitmap(self):
		for entry in self.root_dir.entries:
			if entry.entry_type == ABDE:
				self.allocation_bitmap = AllocationBitmap(self.get_clusters(self.fat.get_cluster_chain(entry.entry.first_cluster)), entry.entry.data_length)
				break

	def get_clusters(self, cluster_list):
		clusters_data = ""
		for cluster in cluster_list:
			cluster_start = (self.vbr.cluster_heap_offset * (2**self.vbr.bytes_per_sector)) + ((cluster-CLUSTER_START) * (2**self.vbr.sectors_per_cluster) * (2**self.vbr.bytes_per_sector))
			cluster_end = cluster_start + ((2**self.vbr.sectors_per_cluster) * (2**self.vbr.bytes_per_sector))
			clusters_data = clusters_data + self.payload[cluster_start:cluster_end]
		return clusters_data

	# XXX TODO
	def list_files(self):
		return self.search_files(self.root_dir.entries)
	# 	# Search files starting from root directory
	# 	file_list = self.search_files(self.root_dir.entries)
	# 	result = ""
	# 	for f in file_list:
	# 		# If f is a dir
	# 		if isinstance(f, list):
	# 			return result + self.list_files(f, init_tab+1)
	# 		else:
	# 			return result + "\t"*init_tab + f
	# 	return result

	def search_files(self, entries):
		files = []
		for entry in entries:
			if isinstance(entry, FileEntrySet):
				file_name = ""
				for f in entry.fnede:
					file_name = file_name + f.entry.file_name
				attributes = entry.fde.entry.get_attributes()
				is_allocated = "" if self.is_cluster_allocated(entry.sede.entry.first_cluster) else "*"
				files.append(is_allocated + file_name + " | " + attributes)
				# Extra infos

				if entry.fde.entry.is_directory():
					entry_cluster_list = self.fat.get_cluster_chain(entry.sede.entry.first_cluster)
					clusters_raw = self.get_clusters(entry_cluster_list)
					files.append(self.search_files(self.get_entries(clusters_raw)))
		return files

	def get_entries(self, clusters_raw):
		# XXX Optimization needed here
		# We still create/treat SEDE and FNEDE objects even though we still have treated them for File Entry Sets
		entries = []
		for i in range(0, len(clusters_raw), 32):
			entry = Entry(clusters_raw[i:i+32])
			if entry.entry_type == FDE:
				file_entry_set_offset = i
				stream_extension_directory_entry_offset = file_entry_set_offset+32
				file_name_extension_directory_entries_offset = stream_extension_directory_entry_offset+32
				# SEDE entry
				stream_extension_directory_entry = Entry(clusters_raw[stream_extension_directory_entry_offset:stream_extension_directory_entry_offset+32])
				# FNEDE entries
				file_name_extension_directory_entries = []
				# Iterates through possible file name extension directory entries.
				# There is a maximum of 17 file name extension directory entries.
				for j in range(file_name_extension_directory_entries_offset, file_name_extension_directory_entries_offset+(17*32), 32):
					file_name_extension_directory_entry = Entry(clusters_raw[j:j+32])
					if file_name_extension_directory_entry.entry_type == FNEDE:
						file_name_extension_directory_entries.append(file_name_extension_directory_entry)
					else:
						break
				file_entry_set = FileEntrySet(entry, stream_extension_directory_entry, file_name_extension_directory_entries)
				entries.append(file_entry_set)
			elif entry.entry_type != SEDE and entry.entry_type != FNEDE:
				entries.append(entry)
		return entries

	def is_cluster_allocated(self, cluster):
		return True if int(self.allocation_bitmap.allocation_bitmap[cluster-CLUSTER_START]) else False
