#!/usr/bin/env python

from entry_types import *
from FileEntrySet import *

class RootDir(object):

	def __init__(self, entries):
		self.entries = entries

	def __repr__(self):
		output = ""
		for entry in self.entries:
			output = output + (entry.__repr__() if entry.__repr__() else "")
		return output