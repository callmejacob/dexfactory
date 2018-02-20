# -- coding: utf-8 --

from common import *

class BytesObject(object):
	"""
	字节数组对象，该对象包含一段字节数组，主要用于字节数组的解析和压缩
	"""

	def __init__(self, bytes):
		"""
		bytes: 原始字节数组
		"""
		self.setBytes(np.array(bytes).astype(np.ubyte))

	def copyFrom(self, bytes):
		"""
		bytes: 原始字节数组，从该数组拷贝到Item项的字节数组中
		"""
		self.bytes[0:self.bytes_size] = bytes[0:self.bytes_size]

	def setBytes(self, bytes):
		"""
		设置字节数组
		bytes: 新的字节数组
		"""
		self.bytes = bytes
		self.bytes_size = len(bytes)

	def getBytes(self):
		"""
		返回字节数组
		"""
		return self.bytes

	def getBytesSize(self):
		"""
		返回字节数组大小
		"""
		return self.bytes_size

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		pass

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		pass

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		pass

	def tohexstring(self):
		"""
		转换为十六进制字符串
		"""
		return convertBytesToHexStr(self.bytes)



class BaseData(BytesObject):
	''' 基础数据类 '''

	def __init__(self, bytes):
		super(BaseData, self).__init__(bytes)

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		pass

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		pass		

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		pass

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		pass