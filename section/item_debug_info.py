# -- coding: utf-8 --

from item_base import *

class DebugInfoItem(BaseItem):
	"""
	section子结构: code_item
	"""

	@classmethod
  	def create(cls):
  		"""
  		创建一个新项
  		"""
  		return DebugInfoItem(createBytes(0x10))

	def __init__(self, bytes):
		"""
		初始化
		bytes:  原始字节数组
		"""
		super(DebugInfoItem, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		off = 0x00

		self.line_start, read_size        =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		self.parameters_size, read_size   =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		self.parameter_names = []
		for i in range(self.parameters_size):
			name_id, read_size = convertUleb128BytesToInt(bytes[off:off+0x05])
			self.parameter_names.append(name_id)
			off += read_size

		# 越过[0x07, 0x0e]
		off += 0x02

		end_index = 0
		while True:
			if bytes[off+end_index] == 0:
				off += end_index + 1
				break
			end_index += 1

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		pass

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''

		string += '%.4d' % self.getBytesSize()
		string += ' [%s]' % self.tohexstring()

		return string

