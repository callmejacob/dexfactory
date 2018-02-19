# -- coding: utf-8 --

from tool import *

class ChunkClassLookupItem(object):
	"""
	类索引的子项结构
	struct ClassLookupItem {
		u4 hash;                 // 类名的hash值
		u4 class_name_off;       // 类名的偏移量
		u4 class_def_off;        // 类定义的偏移量
	}
	"""

	def __init__(self, bytes):

		self.hash              =    convertBytesToInt(bytes[0x00:0x04])
		self.class_name_off    =    convertBytesToInt(bytes[0x04:0x08])
		self.class_def_off     =    convertBytesToInt(bytes[0x08:0x0c])

		self.bytes = bytes[0x00:0x0c]

	def tostring(self):
		string = ''
		string += ' ' * 12 + 'hash:             %.4x\n' % self.hash
		string += ' ' * 12 + 'name_off:         %.4x\n' % self.class_name_off
		string += ' ' * 12 + 'class_def_off:    %.4x\n' % self.class_def_off
		return string


class OdexOptChunkClassLookup(object):
	"""
	类索引结构
	struct ClassLookup {
		u4 total_size;                       // 总字节数，包含total_size, item_size和table在内
		u4 item_size;                        // 子项数目
		ClassLookupItem table[item_size];    // 子项表
	}
	"""

	def __init__(self, bytes):

		self.total_size = convertBytesToInt(bytes[0x00:0x04])
		self.item_size = convertBytesToInt(bytes[0x04:0x08])
		self.item_list = []

		off = 0x08
		for i in range(self.item_size):
			item = ChunkClassLookupItem(bytes[off:off+0x0c])
			self.item_list.append(item)
			off += 0x0c

		self.bytes = bytes[0x00:off]

	def tostring(self):
		string = ''
		# string += 'total_size: %.4x\n' % self.total_size
		string += ' ' * 4 + 'item_size: %.4x\n' % self.item_size
		if self.item_size > 0:
			string += ' ' * 4 + '[\n'
			for item in self.item_list:
				string += ' ' * 8 + '[\n'
				string += item.tostring() 
				string += ' ' * 8 + ']\n'
			string += ' ' * 4 + ']\n'
		return string








