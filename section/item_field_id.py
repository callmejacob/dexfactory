# -- coding: utf-8 --

from item_base import *

class FieldIdItem(BaseItem):
	"""
	属性项
	"""

	@classmethod
  	def create(cls):
  		"""
  		创建一个新项
  		"""
  		return FieldIdItem(createBytes(0x08))

	def __init__(self, bytes):
		"""
		初始化
		bytes:  原始字节数组
		"""
		super(FieldIdItem, self).__init__(bytes[0x00:0x08])

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.class_id =  convertBytesToShort(bytes[0x00:0x02])
		self.type_id =   convertBytesToShort(bytes[0x02:0x04])
		self.name_id =   convertBytesToInt(bytes[0x04:0x08])

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:0x08])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		bytes[0x00:0x02] = convertShortToBytes(self.class_id)
		bytes[0x02:0x04] = convertShortToBytes(self.type_id)
		bytes[0x04:0x08] = convertIntToBytes(self.name_id)

	def getClassId(self):
		"""
		获取类id
		"""
		return self.class_id

	def getTypeId(self):
		"""
		获取类型id
		"""
		return self.type_id

	def getNameId(self):
		"""
		获取名称id
		"""
		return self.name_id

	def setClassId(self, class_id):
		"""
		设置类id
		class_id: 类id
		"""
		self.class_id = class_id
		self.encode()

	def setTypeId(self, type_id):
		"""
		设置类型id
		type_id: 类型id
		"""
		self.type_id = type_id
		self.encode()

	def setNameId(self, name_id):
		"""
		设置名称id
		name_id: 名称id
		"""
		self.name_id = name_id
		self.encode()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		return 'class: %.4d, type: %.4d, name: %.4d' % (self.class_id, self.type_id, self.name_id)