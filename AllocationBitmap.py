#!/usr/bin/env python

import struct

class AllocationBitmap(object):

	def __init__(self, payload, allocation_bitmap_size_in_bytes):
		self.allocation_bitmap = ""
		# !! There could be some extra bits at the end of the allocation bitmap string (if (nb of clusters-2) % 8 != 0)
		for idx, byte in enumerate(payload):
			self.allocation_bitmap = self.allocation_bitmap + "{0:08b}".format(struct.unpack("<B",byte)[0])[::-1]
			if idx+1 == allocation_bitmap_size_in_bytes:
				break