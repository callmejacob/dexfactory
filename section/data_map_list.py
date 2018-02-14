# -- coding: utf-8 --

from data_base import *


class MapListItemData(BaseData):
	"""
	MapListItem中的数据项
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return MapListItemData(createBytes(0x0c))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(MapListItemData, self).__init__(bytes[0x00:0x0c])

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		self.type =     convertBytesToShort(bytes[0x00:0x02])
		self.unused =   convertBytesToShort(bytes[0x02:0x04])
		self.size =     convertBytesToInt(bytes[0x04:0x08])
		self.off =      convertBytesToInt(bytes[0x08:0x0c])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

		bytes[0x00:0x02] = convertShortToBytes(self.type)
		bytes[0x02:0x04] = convertShortToBytes(self.unused)
		bytes[0x04:0x08] = convertIntToBytes(self.size)
		bytes[0x08:0x0c] = convertIntToBytes(self.off)

	def getSectionType(self):
		"""
		获取section类型
		"""
		return self.type

	def getSectionItemSize(self):
		"""
		获取子项个数
		"""
		return self.size

	def getSectionOff(self):
		"""
		获取section偏移
		"""
		return self.off

	def setSectionType(self, type):
		"""
		设置section类型
		type:    section类型
		"""
		self.type = type
		self.encode()

	def setSectionItemSize(self, size):
		"""
		设置section的子项个数
		size:    section的子项个数
		"""
		self.size = size
		self.encode()

	def setSectionOff(self, off):
		"""
		设置section的偏移
		off:     section基于文件的偏移量
		"""
		self.off = off
		self.encode()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		return 'type: %.4x, size: %.4x, off: %.4x, bytes: %s' % (self.type, self.size, self.off, self.tohexstring())
