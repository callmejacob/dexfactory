# -- coding: utf-8 --

from tool import *


class MethodRegisterMapItem(object):
	"""
	寄存器映射子项
	struct RegisterMapItem {
		u1/u2 cur_insns_index;               // 当前指令索引，从0开始
		u1/u2 cur_insns_registers_status;    // 当前指令的寄存器状态，每位记录了对应寄存器是否引用对象，1表示引用，0表示不引用
	}
	"""

	def __init__(self, index_width, reg_width, bytes):

		off = 0x00

		if index_width == 1:
			self.cur_insns_index = (byte[off] << 0)
			off += 0x01
		else:
			self.cur_insns_index = (bytes[off] << 0) | (bytes[off+0x01] << 8)
			off += 0x02

		if reg_width == 1:
			self.cur_insns_registers_status = (bytes[off] << 0)
			off += 0x01
		else:
			self.cur_insns_registers_status = (bytes[off] << 0) | (bytes[off+0x01] << 8)
			off += 0x02

		self.bytes = byte[0x00:off]

	def tostring(self):
		string = ''
		string += '{\n'
		string += ' ' * 4 + 'cur_insns_index:               %.2x\n' % self.cur_insns_index
		string += ' ' * 4 + 'cur_insns_registers_status:    %.2x\n' % self.cur_insns_registers_status
		string += '}\n'
		return string


"""
寄存器映射的指令保存格式
"""
REGISTER_MAP_FORMAT_UNKNOWN         =    0x00
REGISTER_MAP_FORMAT_NONE            =    0x01
REGISTER_MAP_FORMAT_COMPACT8        =    0x02
REGISTER_MAP_FORMAT_COMPACT16       =    0x03
REGISTER_MAP_FORMAT_DIFFERENTIAL    =    0x04
REGISTER_MAP_FORMAT_ONHEAP          =    0x80
  

class MethodRegisterMap(object):
	"""
	寄存器映射
	struct RegisterMap {
		u1                       insns_format;            // 指令格式
		u1                       reg_width;               // 寄存器状态占用的字节数
		u2                       item_size;               // 子项列表个数
		MethodRegisterMapItem    item_list[item_size];    // 子项列表
	}
	"""

	def __init__(self, bytes):

		# 解析格式, 如果是非法或者空格式，直接返回
		self.format = bytes[0x00]

		if self.format == REGISTER_MAP_FORMAT_UNKNOWN or self.format == REGISTER_MAP_FORMAT_NONE:
			self.bytes = bytes[0x00:0x01]
			return

		# 解析其它字段
		self.reg_width = bytes[0x01]
		self.item_size = (bytes[0x02] << 0) | (bytes[0x03] << 8)
		self.item_list = []

		# 解析数据列表
		index_width = 1
		if self.format == REGISTER_MAP_FORMAT_COMPACT16:
			index_width = 2

		off = 0x04
		for i in range(self.item_size):
			item = MethodRegisterMapItem(index_width, self.reg_width, bytes[off:])
			self.item_list.append(item)
			off += len(item.bytes)

		# 设置对应的真实字节数组
		self.bytes = bytes[0x00:off]

	def tostring(self):
		string = ''
		string += 'format:       %.2x\n' % self.format
		string += 'reg_width:    %.2x\n' % self.reg_width
		string += 'item_size:    %.4x\n' % self.item_size
		if self.item_size > 0:
			string += '[\n'
			for item in self.item_list:
				string += item.tostring()
			string += ']\n'


class ChunkRegisterMapClassItem(object):
	"""
	寄存器映射中的类子项结构
	struct RegisterMapClassItem {
		u4                   item_size;               // 列表总个数
		MethodRegisterMap    item_list[item_size];    // 方法对应的寄存器映射列表
	}
	"""

	def __init__(self, bytes):

		self.item_size = convertBytesToInt(bytes[0x00:0x04])
		self.item_list = []

		off = 0x04
		for i in range(self.item_size):
			item = MethodRegisterMap(bytes[off:])
			self.item_list.append(item)
			off += len(item.bytes)

		# 四字节对齐
		if off % 0x04 != 0:
			off += 0x04 - (off % 0x04)

		self.bytes = bytes[0x00:off]



class OdexOptChunkRegisterMap(object):
	"""
	寄存器映射结构
	struct RegisterMap {
		u4                      item_size;               // 列表总个数
		u4                      off_list[item_size];     // 类子项列表的偏移列表
		RegisterMapClassItem    item_list[item_size];    // 类子项列表
	}
	"""

	def __init__(self, bytes):

		self.item_size = convertBytesToInt(bytes[0x00:0x04])
		self.off_list = []
		self.item_list = []

		off = 0x04
		for i in range(self.item_size):
			off_item = convertBytesToInt(bytes[off:off+0x04])
			self.off_list.append(off_item)
			off += 0x04

		for off_item in self.off_list:
			item = ChunkRegisterMapClassItem(bytes[off_item:])
			self.item_list.append(item)
			off += len(item.bytes)

		self.bytes = bytes[0x00:off]

	def tostring(self):
		return ''



