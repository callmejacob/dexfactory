# -- coding: utf-8 --

from opt_chunk_class_lookup import *
from opt_chunk_register_map import *

"""
定义chunk类型
"""
OPT_CHUNK_TYPE_CLASS_LOOK_UP    =    0x434c4b50
OPT_CHUNK_TYPE_REGISTER_MAPS    =    0x524d4150
OPT_CHUNK_TYPE_END              =    0x41454e44


"""
定义chunk的类型描述映射
"""
chunk_desc_map = {

	OPT_CHUNK_TYPE_CLASS_LOOK_UP    :    'class_look_up',
	OPT_CHUNK_TYPE_REGISTER_MAPS    :    'register_maps',
	OPT_CHUNK_TYPE_END              :    'end',

}


class OdexOptChunk(object):
	"""
	odex文件中opt部分的chunk块
	"""

	def __init__(self, bytes):

		self.chunk_type = convertBytesToInt(bytes[0x00:0x04])
		self.chunk_size = convertBytesToInt(bytes[0x04:0x08])

		self.chunk_data = None
		if self.chunk_type == OPT_CHUNK_TYPE_CLASS_LOOK_UP:
			self.chunk_data = OdexOptChunkClassLookup(bytes[0x08:0x08+self.chunk_size])
		elif self.chunk_type == OPT_CHUNK_TYPE_REGISTER_MAPS:
			self.chunk_data = OdexOptChunkRegisterMap(bytes[0x08:0x08+self.chunk_size])
		elif self.chunk_type == OPT_CHUNK_TYPE_REGISTER_MAPS:
			pass

		self.bytes = bytes[0x00:0x08+self.chunk_size]

	def tostring(self):
		string = ''
		string += "chunk '%s': {\n" % chunk_desc_map[self.chunk_type]
		string += ' ' * 4 + 'bytes_size: %.4x\n' % self.chunk_size
		if self.chunk_data:
			string += self.chunk_data.tostring()
		string += '}\n'
		return string