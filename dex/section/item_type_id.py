# -- coding: utf-8 --

from item_base import *

class TypeIdItem(BaseItem):
	"""
	section子结构: 类型ID项
	"""

	@classmethod
	def create(cls):
		"""
		创建项
		"""
		return TypeIdItem(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(TypeIdItem, self).__init__(bytes[0x00:0x04])

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.string_id = convertBytesToInt(bytes[0x00:0x04])

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:0x04])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		bytes[0x00:0x04]  = convertIntToBytes(self.string_id)

	def tostring(self):
		"""
		转化为可打印的字符串
		"""
		string = '%.4d' % self.string_id
		return string