# -- coding: utf-8 --

from item_base import *

class StringIdItem(BaseItem):
	"""
	section子结构: 字符串ID项
	"""

	@classmethod
	def create(cls):
		"""
		创建项
		"""
		return StringIdItem(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(StringIdItem, self).__init__(bytes[0x00:0x04])

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.string_data_off = convertBytesToInt(bytes[0x00:0x04])
		self.string_data_id = -1
		self.string_data_item = None

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:0x04])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		bytes[0x00:0x04]  = convertIntToBytes(self.string_data_off)

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		self.string_data_id = context.getSectionItemIdByOff(TYPE_STRING_DATA_ITEM, self.string_data_off)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		self.string_data_off = context.getSectionItemOffById(TYPE_STRING_DATA_ITEM, self.string_data_id)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		self.string_data_item = context.getSectionItemById(TYPE_STRING_DATA_ITEM, self.string_data_id)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		self.string_data_id = context.getSectionIdByItem(TYPE_STRING_DATA_ITEM, self.string_data_item)

	def tostring(self):
		"""
		转化为可打印的字符串
		"""
		string = '[%.4x %.4d]' % (self.string_data_off, self.string_data_id)
		return string
