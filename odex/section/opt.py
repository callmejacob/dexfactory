# -- coding: utf-8 --

from opt_chunk import *

class OdexOpt(object):
	"""
	odex中的opt部分
	"""

	def __init__(self, bytes):

		self.chunk_list = []

		off = 0x00
		while True:
			chunk = OdexOptChunk(bytes[off:])
			self.chunk_list.append(chunk)
			off += len(chunk.bytes)

			if chunk.chunk_type == OPT_CHUNK_TYPE_END:
				break

		self.bytes = bytes[0x00:off]

	def tostring(self):
		string = 'opt: {\n'

		for chunk in self.chunk_list:
			string += chunk.tostring()

		string += '}\n'
		return string




