# -- coding: utf-8 --

from item_base import *

class EncodedArrayItem(BaseItem):
	"""
	section子结构: encoded_array_item
	"""

	@classmethod
  	def create(cls):
  		"""
  		创建一个新项
  		"""
  		return EncodedArrayItem(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:  原始字节数组
		"""
		super(EncodedArrayItem, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.value = EncodedArrayData(bytes)

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:self.value.getBytesSize()])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		# 调整尺寸
		new_size = self.value.getBytesSize()
		if self.getBytesSize != new_size:
			self.setBytes(createBytes(new_size))

		# 编码
		bytes = self.getBytes()

		bytes[0x00:self.value.getBytesSize()] = self.value.getBytes()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''
		string += self.value.tostring()
		return string
