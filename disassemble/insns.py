# -- coding: utf-8 --

from insns_item import *

class Insns(object):
	"""
	反汇编
	"""

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节码的字节数组
		"""
		self.bytes = bytes

		self.decode()

	def decode(self):
		"""
		解码
		"""
		bytes = self.bytes

		self.item_list = []

		off = 0x00
		while off < len(bytes):
			item = InsnsItem(bytes[off:])
			self.item_list.append(item)
			off += item.bytes_size

	def tostring(self, context = None):
		"""
		转换成字符串
		"""
		string = ''

		if context is None:
			for item in self.item_list:
				string += item.tostring() + '\n'
		else:
			for item in self.item_list:
				kind, kind_x, proto_x = item.getKindInfo()
				kind_desc = getKindDesc(context, kind, kind_x)
				proto_desc = getKindDesc(context, KIND_PROTO, proto_x)
				format_string = item.format(kind_desc, proto_desc)
				if format_string is None:
					string += item.tostring() + '\n'
				else:
					string += format_string + '\n'

		return string