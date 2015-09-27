#!/usr/bin/env python

from Entry import *

class FileEntrySet(object):

	def __init__(self, fde, sede, fnede):
		self.fde = fde
		self.sede = sede
		self.fnede = fnede		# List of File Name Extension Directory Entry

	def __repr__(self):
		return "\n(File Entry Set)\n" + self.fde.__repr__() + self.sede.__repr__() + self.fnede.__repr__() + "\n"