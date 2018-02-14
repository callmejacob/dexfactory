# -- coding: utf-8 --

from data_base import *


class TypeListItemData(BaseData):
	"""
	类型列表中的子类型结构数据
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return TypeListItemData(createBytes(0x02))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(TypeListItemData, self).__init__(bytes[0x00:0x02])

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		self.type_id = convertBytesToShort(bytes[0x00:0x02])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

		bytes[0x00:0x02] = convertShortToBytes(self.type_id)

	def getTypeId(self):
		"""
		获取类型id
		"""
		return self.type_id

	def setTypeId(self, type_id):
		"""
		设置类型id
		type_id:    类型id
		"""
		self.type_id = type_id
		self.encode()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		return 'type: %.4x' % self.type_id