# -- coding: utf-8 --

from section_base import *

class FieldIdListSection(BaseSection):
	"""
	section: field ids列表
	"""

	def __init__(self, context, bytes, size, off):
		"""
		初始化
		context:    上下文信息
		bytes:      原始字节数组
		size:       项列表的总个数
		off:        字节数组偏移
		"""
		super(FieldIdListSection, self).__init__(context, TYPE_FIELD_ID_ITEM, bytes[off:], size)

	def getItemDesc(self, index):
		"""
		获取proto id的字符串描述
		index: 索引
		"""
		if index >= self.item_size:
			return ''

		item = self.item_list[index]

		class_string = self.getContextDesc(TYPE_TYPE_ID_ITEM, item.getClassId())
		type_string = self.getContextDesc(TYPE_TYPE_ID_ITEM, item.getTypeId())
		name_string = self.getContextDesc(TYPE_STRING_DATA_ITEM, item.getNameId())

		return '%s -> %s { %s }' % (class_string, name_string, type_string)