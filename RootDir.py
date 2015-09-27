#!/usr/bin/env python

from Entry import *
from FileEntrySet import *

class RootDir(object):

	def __init__(self, entries, deleted_entries):
		self.entries = entries
		self.deleted_entries = deleted_entries

	def __repr__(self):
		output = ""
		for entry in self.entries:
			output = output + (entry.__repr__() if entry.__repr__() else "")
		return output