# -- coding: utf-8 --

from section_base import *

class TypeListSection(BaseSection):
	"""
	section: 类型id列表
	"""

	def __init__(self, context, bytes, size, off):
		"""
		初始化
		context:    上下文信息
		bytes:      原始字节数组
		size:       项列表的总个数
		off:        字节数组偏移
		"""
		super(TypeListSection, self).__init__(context, TYPE_TYPE_LIST, bytes[off:], size)

	def decode(self):
		"""
		解码字节数组:  比较特殊的section，每项要求四字节对齐，但是最后一项不需要
		"""
		super(TypeListSection, self).decode()

		if self.item_size > 0:
			last_item = self.getItem(self.item_size - 1)

			if last_item.item_size % 0x02 != 0:
				bytes = self.getBytes()
				bytes_size = self.getBytesSize()
				self.setBytes(bytes[0x00:bytes_size-0x02])

	def encode(self):
		"""
		编码字节数组
		"""
		super(TypeListSection, self).encode()

		if self.item_size > 0:
			last_item = self.getItem(self.item_size - 1)

			if last_item.item_size % 0x02 != 0:
				bytes = self.getBytes()
				bytes_size = self.getBytesSize()
				self.setBytes(bytes[0x00:bytes_size-0x02])

	def getItemDesc(self, index):
		"""
		获取类型字符串
		index:  索引
		"""
		if index < self.item_size:
			item = self.item_list[index]
			item_data_list = item.getItemDataList()

			string = ''
			for item_data in item_data_list:
				type_id = item_data.getTypeId()
				string += self.getContextDesc(TYPE_TYPE_ID_ITEM, type_id) + ' '

			return string

		return '%.4d' % index