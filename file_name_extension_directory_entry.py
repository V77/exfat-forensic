#!/usr/bin/python

class FileNameExtensionDirectoryEntry :
	def __init__ (self, content) :
		self.content=content

	def get_entry_type(self):
		end_offset = 2
		return self.content [:end_offset]

	def get_general_secondary_flags(self):
		start_offset=2
		end_offset=4
		return self.content[start_offset:end_offset]

	def get_file_name(self):
		start_offset=4
		end_offset=64
		return self.content[start_offset:end_offset]

filename = "/home/douby/extfat_project/disk1.001"
d=open(filename, 'rb')
#offset fichier installer.txt = 0x296a0 = 169632
content = d.read()[169632:171000]
content_hex = content.encode("hex")

file_name_extension_directory_entry=FileNameExtensionDirectoryEntry(content_hex)
print "Entry Type : " +  file_name_extension_directory_entry.get_entry_type()
print "General Secondary Flags : " + file_name_extension_directory_entry.get_general_secondary_flags()
print "File Name : " + file_name_extension_directory_entry.get_file_name().decode("hex")
