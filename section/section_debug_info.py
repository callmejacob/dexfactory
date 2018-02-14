# -- coding: utf-8 --

from section_base import *

class DebugInfoSection(BaseSection):
	"""
	section: debug_info_item
	"""

	def __init__(self, context, bytes, size, off):
		"""
		初始化
		context:   上下文信息
		bytes:     原始字节数组
		size:      子项总个数
		off:       字节数组偏移
		"""
		super(DebugInfoSection, self).__init__(context, TYPE_DEBUG_INFO_ITEM, bytes[off:], size)

	# def decode(self):
	# 	"""
	# 	解码字节数组
	# 	"""
	# 	bytes = self.getBytes()

	# 	self.item_list = []

	# def encode(self):
	# 	"""
	# 	编码字节数组
	# 	"""
	# 	pass

	# def getItemDesc(self, index):
	# 	"""
	# 	获取子项的字符串描述
	# 	index: 索引
	# 	"""
	# 	return '%.4d' % index

	# def tostring(self):
	# 	return 'TYPE_DEBUG_INFO_ITEM: %.4x' % TYPE_DEBUG_INFO_ITEM, self.tohexstring()