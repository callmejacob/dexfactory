# -- coding: utf-8 --

from item_base import *

class StringDataItem(BaseItem):
	"""
	section子结构: 字符串项
	"""

	@classmethod
	def create(cls):
		"""
		创建项
		"""
		return StringDataItem(createBytes(0x02))

	def __init__(self, bytes):
		"""
		初始化
		bytes:  原始字节数组，结构为[size, string, 0]，所以大小为1 + size + 1 = size + 2
		"""
		super(StringDataItem, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.string_size    =    bytes[0x00]
		self.string_data    =    bytes[0x01:0x01+self.string_size].tostring()

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:self.string_size+0x02])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		# 检测字符串大小是否有变化
		if len(self.string_data) != self.string_size:
			self.string_size = len(self.string_data)
			self.setBytes(createBytes(self.string_size+0x02))

		bytes = self.getBytes()

		bytes[0x00]                          =    self.string_size
		bytes[0x01:0x01+self.string_size]    =    convertStringToBytes(self.string_data)
		bytes[self.string_size+0x01]         =    0x00

	def setString(self, string):
		"""
		设置字符串
		string: 字符串
		"""
		self.string_data = string
		self.encode()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		return self.string_data
