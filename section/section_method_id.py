# -- coding: utf-8 --

from section_base import *

class MethodIdListSection(BaseSection):
	"""
	section: method ids列表
	"""

	def __init__(self, context, bytes, size, off):
		"""
		初始化
		context:    上下文信息
		bytes:      原始字节数组
		size:       项列表的总个数
		off:        字节数组偏移
		"""
		super(MethodIdListSection, self).__init__(context, TYPE_METHOD_ID_ITEM, bytes[off:], size)

	def getItemDesc(self, index):
		"""
		获取proto id的字符串描述
		index: 索引
		"""
		if index >= self.item_size:
			return ''

		item = self.item_list[index]

		class_string = self.getContextDesc(TYPE_TYPE_ID_ITEM, item.getClassId())
		proto_string = self.getContextDesc(TYPE_PROTO_ID_ITEM, item.getProtoId())
		name_string = self.getContextDesc(TYPE_STRING_DATA_ITEM, item.getNameId())

		return 'class: %s proto: [%s] name: %s' % (class_string, proto_string, name_string)