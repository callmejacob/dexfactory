# -- coding: utf-8 --

from section_base import *

class MapItemListSection(BaseSection):
	"""
	section: map 项列表
	"""

	def __init__(self, context, bytes, size, off):
		"""
		初始化
		context:    上下文信息
		bytes:      原始字节数组
		size:       子项总个数
		off:        字节数组偏移
		"""
		super(MapItemListSection, self).__init__(context, TYPE_MAP_LIST, bytes[off:], size)

	def getItemDataList(self):
		"""
		获取子项的数据列表，每一项代表一个section的信息
		"""
		return self.getItem(0).getItemDataList()