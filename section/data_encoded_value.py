# -- coding: utf-8 --

from data_base import *

'''
定义编码类型
'''
ENCODED_VALUE_BYTE             =    0x00
ENCODED_VALUE_SHORT            =    0x02
ENCODED_VALUE_CHAR             =    0x03
ENCODED_VALUE_INT              =    0x04
ENCODED_VALUE_LONG             =    0x06
ENCODED_VALUE_FLOAT            =    0x10
ENCODED_VALUE_DOUBLE           =    0x11
ENCODED_VALUE_METHOD_TYPE      =    0x15
ENCODED_VALUE_METHOD_HANDLE    =    0x16
ENCODED_VALUE_STRING           =    0x17
ENCODED_VALUE_TYPE             =    0x18
ENCODED_VALUE_FIELD            =    0x19
ENCODED_VALUE_METHOD           =    0x1a
ENCODED_VALUE_ENUM             =    0x1b
ENCODED_VALUE_ARRAY            =    0x1c
ENCODED_VALUE_ANNOTATION       =    0x1d
ENCODED_VALUE_NULL             =    0x1e
ENCODED_VALUE_BOOLEAN          =    0x1f



'''
映射表，用于记录EncodedValue类型的解析类， 格式[value_type : encoded_value_class]
'''
encoded_value_class_map = {

	ENCODED_VALUE_ARRAY            :	None,
	ENCODED_VALUE_ANNOTATION       :    None,

}



class EncodedValueData(BaseData):
	"""
	data: encoded_value
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return EncodedValueData(createBytes(0x01))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(EncodedValueData, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		# 解析type和arg
		self.value_type  = (bytes[0x00] >> 0) & 0x1f
		self.value_arg   = (bytes[0x00] >> 5) & 0x07

		# 解析value
		self.value = None

		if self.value_type == ENCODED_VALUE_BYTE:
			self.value = BytesObject(bytes[0x01])
		elif self.value_type <= ENCODED_VALUE_ENUM:
			self.value = BytesObject(bytes[0x01:0x01+(self.value_arg+0x01)])
		elif self.value_type == ENCODED_VALUE_ARRAY or self.value_type == ENCODED_VALUE_ANNOTATION:
			encoded_value_class = encoded_value_class_map[self.value_type]
			if encoded_value_class:
				self.value = encoded_value_class(bytes[0x01:])

		# 重新调整字节数组大小
		size = 0x01
		if self.value:
			size += self.value.getBytesSize()
		self.setBytes(bytes[0x00:size])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''

		string += 'type: %.2x' % self.value_type
		string += ' arg: %.2d' % self.value_arg
		if self.value_type == ENCODED_VALUE_ARRAY or self.value_type == ENCODED_VALUE_ANNOTATION:
			if self.value:
				string += ' value: %s' % self.value.tostring()
		elif self.value:
			string += ' value: %s' % self.value.tohexstring()

		return string


class AnnotationElementData(BaseData):
	"""
	data: annotation_element
	"""

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(AnnotationElementData, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		off = 0x00

		self.name_id, read_size = convertUleb128BytesToInt(bytes[off:])
		off += read_size

		self.value = EncodedValueData(bytes[off:])
		off += self.value.getBytesSize()

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''

		string += 'name_id: %.4d' % self.name_id
		string += ' value: %s' % self.value.tostring()

		return string		



class EncodedAnnotationData(BaseData):
	"""
	data: encoded_annotation
	"""

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(EncodedAnnotationData, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		off = 0x00

		self.type_id, read_size = convertUleb128BytesToInt(bytes[off:])
		off += read_size

		self.item_size, read_size = convertUleb128BytesToInt(bytes[off:])
		off += read_size

		# 解析子项列表
		self.item_list = []

		for i in range(self.item_size):
			item = AnnotationElementData(bytes[off:])
			self.item_list.append(item)
			off += item.getBytesSize()

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

	def getItemDataList(self):
		"""
		返回数据列表
		"""
		return self.item_list

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = '{\n'

		string += 'type_id: %.4d\n' % self.type_id
		string += 'item_size: %.4d\n' % self.item_size
		if self.item_size > 0:
			for item in self.item_list:
				string += '    %s\n' % item.tostring()

		string += '}\n'

		return string			


class EncodedArrayData(BaseData):
	"""
	data: encoded_annotation
	"""

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(EncodedArrayData, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		off = 0x00

		self.item_size, read_size = convertUleb128BytesToInt(bytes[off:])
		off += read_size

		# 解析子项列表
		self.item_list = []

		for i in range(self.item_size):
			item = EncodedValueData(bytes[off:])
			self.item_list.append(item)
			off += item.getBytesSize()

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

	def getItemDataList(self):
		"""
		返回数据列表
		"""
		return self.item_list

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = '{\n'

		string += 'item_size: %.4d\n' % self.item_size
		if self.item_size > 0:
			for item in self.item_list:
				string += '    %s\n' % item.tostring()

		string += '}\n'

		return string		



'''
记录映射值
'''
encoded_value_class_map[ENCODED_VALUE_ANNOTATION] = EncodedAnnotationData
encoded_value_class_map[ENCODED_VALUE_ARRAY]      = EncodedArrayData