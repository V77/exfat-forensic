#!/usr/bin/python

class VolumeLabelDirectoryEntry :
	def __init__(self, content):
		self.content=content

	def get_entry_type(self):
		end_offset = 2
		return self.content[:end_offset]

	def get_character_count(self):
		start_offset = 2
		end_offset = 4
		return self.content[start_offset:end_offset]

	def get_volume_label(self):
		start_offset = 4
		end_offset = 50
		return self.content[start_offset:end_offset]

	def get_reserved(self):
		start_offset = 50
		end_offset = 64
		return self.content[start_offset:end_offset]

filename = "/home/douby/extfat_project/disk1.001"
d=open(filename, 'rb')
content = d.read()[169472:169506]
content_hex = content.encode("hex")

volume_label_directory_entry=VolumeLabelDirectoryEntry(content_hex)
print "Entry Type : " + volume_label_directory_entry.get_entry_type()
print "Character Count : " + volume_label_directory_entry.get_character_count()
print "Volume Label : " + volume_label_directory_entry.get_volume_label().strip().decode("hex")
print "Reserved : " + volume_label_directory_entry.get_reserved()
