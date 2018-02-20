# -- coding: utf-8 --

from data_base import *


class ClassDataItemFieldData(BaseData):
	"""
	类数据中的field结构
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return ClassDataItemFieldData(createBytes(0x02))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(ClassDataItemFieldData, self).__init__(bytes[0x00:0x0a])

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		off = 0x00

		self.field_id_diff, read_size    =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		self.access_flags, read_size      =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		# field_id需要通过field_id_diff还原回来
		self.field_id = 0

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

		off = 0

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.field_id_diff)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.access_flags)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

	def getFieldIdDiff(self):
		"""
		获取field的id差值
		"""
		return self.field_id_diff

	def getAccessFlags(self):
		"""
		获取属性flags
		"""
		return self.access_flags

	def getFieldId(self):
		"""
		获取field的id值
		"""
		return self.field_id

	def setFieldIdDiff(self, field_id_diff):
		"""
		设置field的id差值
		field_id_diff:    field的id差值
		"""
		self.field_id_diff = field_id_diff
		self.encode()

	def setAccessFlags(self, access_flags):
		"""
		获取属性flags
		access_flags:     属性flags
		"""
		self.access_flags = access_flags
		self.encode()

	def setFieldId(self, field_id):
		"""
		获取field的id差值
		field_id:         field的id差值
		"""
		self.field_id = field_id

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''
		string += 'field: [%.4d, %.4d]' % (self.field_id_diff, self.field_id)
		string += ', access_flags: %.4x' % self.access_flags
		return string



class ClassDataItemMethodData(BaseData):
	"""
	类数据中的Method结构
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return ClassDataItemMethodData(createBytes(0x03))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(ClassDataItemMethodData, self).__init__(bytes[0x00:0x0f])

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		off = 0x00

		self.method_id_diff, read_size    =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		self.access_flags, read_size      =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		self.code_off, read_size          =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		# method_id需要通过method_id_diff还原回来
		self.method_id = 0
		self.code_id = -1
		self.code_item = None

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

		off = 0

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.method_id_diff)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.access_flags)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.code_off)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		self.code_id = context.getSectionItemIdByOff(TYPE_CODE_ITEM, self.code_off)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		self.code_off = context.getSectionItemOffById(TYPE_CODE_ITEM, self.code_id)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		self.code_item = context.getSectionItemById(TYPE_CODE_ITEM, self.code_id)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		self.code_id = context.getSectionIdByItem(TYPE_CODE_ITEM, self.code_item)

	def getMethodIdDiff(self):
		"""
		获取method的id差值
		"""
		return self.method_id_diff

	def getAccessFlags(self):
		"""
		获取属性flags
		"""
		return self.access_flags

	def getCodeOff(self):
		"""
		获取代码偏移量
		"""
		return self.code_off

	def getMethodId(self):
		"""
		获取method的id值
		"""
		return self.method_id

	def setMethodIdDiff(self, method_id_diff):
		"""
		设置method的id差值
		method_id_diff:    method的id差值
		"""
		self.method_id_diff = method_id_diff
		self.encode()

	def setAccessFlags(self, access_flags):
		"""
		获取属性flags
		access_flags:     属性flags
		"""
		self.access_flags = access_flags
		self.encode()

	def setCodeOff(self, code_off):
		"""
		设置代码偏移量
		code_off:         代码偏移量
		"""
		self.code_off = code_off
		self.encode()

	def setMethodId(self, method_id):
		"""
		获取method的id差值
		method_id:         method的id差值
		"""
		self.method_id = method_id

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''
		string += 'method: [%.4d %.4d]' % (self.method_id_diff, self.method_id)
		string += ', access_flags: %.4x' % self.access_flags
		string += ', code: [%.4x %.4d]' % (self.code_off, self.code_id)
		string += ', method: %.4d' % self.method_id
		return string
