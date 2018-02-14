# -- coding: utf-8 --

from item_base import *

class ClassDataItem(BaseItem):
	"""
	section子结构: 类数据
	"""

	@classmethod
  	def create(cls):
  		"""
  		创建一个新项
  		"""
  		return ClassDataItem(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:  原始字节数组
		"""
		super(ClassDataItem, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		off = 0x00

		# 解析尺寸
		self.static_field_size, read_size      =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		self.instance_field_size, read_size    =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		self.direct_method_size, read_size     =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		self.virtual_method_size, read_size    =    convertUleb128BytesToInt(bytes[off:off+0x05])
		off += read_size

		# 静态属性列表
		self.static_field_list = []
		for i in range(self.static_field_size):
			item = ClassDataItemFieldData(bytes[off:off+0x0a])
			self.static_field_list.append(item)
			off += item.getBytesSize()

		# 实例属性列表
		self.instance_field_list = []
		for i in range(self.instance_field_size):
			item = ClassDataItemFieldData(bytes[off:off+0x0a])
			self.instance_field_list.append(item)
			off += item.getBytesSize()


		# 直接方法列表
		self.direct_method_list = []
		for i in range(self.direct_method_size):
			item = ClassDataItemMethodData(bytes[off:off+0x0f])
			self.direct_method_list.append(item)
			off += item.getBytesSize()

		# 虚方法列表
		self.virtual_method_list = []
		for i in range(self.virtual_method_size):
			item = ClassDataItemMethodData(bytes[off:off+0x0f])
			self.virtual_method_list.append(item)
			off += item.getBytesSize()
		
		# 根据差值计算真实值
		self.convertDiffToIdForFieldList(self.static_field_list)
		self.convertDiffToIdForFieldList(self.instance_field_list)
		self.convertDiffToIdForMethodList(self.direct_method_list)
		self.convertDiffToIdForMethodList(self.virtual_method_list)

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		# 重新计算四个列表的长度，并从真实值计算差值
		self.static_field_size = len(self.static_field_list)
		self.instance_field_size = len(self.instance_field_list)
		self.direct_method_size = len(self.direct_method_list)
		self.virtual_method_size = len(self.virtual_method_list)

		self.convertIdToDiffForFieldList(self.static_field_list)
		self.convertIdToDiffForFieldList(self.instance_field_list)
		self.convertIdToDiffForMethodList(self.direct_method_list)
		self.convertIdToDiffForMethodList(self.virtual_method_list)

		# 重新计算字节数组大小
		new_size = 0

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.static_field_size)
		new_size += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.instance_field_size)
		new_size += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.direct_method_size)
		new_size += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.virtual_method_size)
		new_size += write_size

		for item in self.static_field_list:
			new_size += item.getBytesSize()

		for item in self.instance_field_list:
			new_size += item.getBytesSize()

		for item in self.direct_method_list:
			new_size += item.getBytesSize()

		for item in self.virtual_method_list:
			new_size += item.getBytesSize()

		# class_data_item没有四字节对齐的要求
		# if new_size % 0x04 != 0:
		# 	new_size += 0x04 - (new_size % 0x04)

		if self.getBytesSize() != new_size:
			self.setBytes(createBytes(new_size))
		else:
			zerosBytes(self.getBytes())

		# 编码
		bytes = self.getBytes()

		off = 0x00

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.static_field_size)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.instance_field_size)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.direct_method_size)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

		uleb128_bytes, write_size = convertIntToUleb128Bytes(self.virtual_method_size)
		bytes[off:off+write_size] = uleb128_bytes
		off += write_size

		for item in self.static_field_list:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

		for item in self.instance_field_list:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

		for item in self.direct_method_list:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

		for item in self.virtual_method_list:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		for item in self.static_field_list:
			item.convertOffToId(context)

		for item in self.instance_field_list:
			item.convertOffToId(context)

		for item in self.direct_method_list:
			item.convertOffToId(context)

		for item in self.virtual_method_list:
			item.convertOffToId(context)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		for item in self.static_field_list:
			item.convertIdToOff(context)

		for item in self.instance_field_list:
			item.convertIdToOff(context)

		for item in self.direct_method_list:
			item.convertIdToOff(context)

		for item in self.virtual_method_list:
			item.convertIdToOff(context)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		for item in self.static_field_list:
			item.convertIdToItem(context)

		for item in self.instance_field_list:
			item.convertIdToItem(context)

		for item in self.direct_method_list:
			item.convertIdToItem(context)

		for item in self.virtual_method_list:
			item.convertIdToItem(context)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		for item in self.static_field_list:
			item.convertItemToId(context)

		for item in self.instance_field_list:
			item.convertItemToId(context)

		for item in self.direct_method_list:
			item.convertItemToId(context)

		for item in self.virtual_method_list:
			item.convertItemToId(context)

	def convertDiffToIdForFieldList(self, field_list):
		"""
		转换field列表的差值到真实值
		"""
		field_id = 0
		for i in range(len(field_list)):
			item = field_list[i]
			if i == 0:
				field_id = item.getFieldIdDiff()
			else:
				field_id += item.getFieldIdDiff()
			item.setFieldId(field_id)

	def convertDiffToIdForMethodList(self, method_list):
		"""
		转换method列表的差值到真实值
		"""
		method_id = 0
		for i in range(len(method_list)):
			item = method_list[i]
			if i == 0:
				method_id = item.getMethodIdDiff()
			else:
				method_id += item.getMethodIdDiff()
			item.setMethodId(method_id)

	def convertIdToDiffForFieldList(self, field_list):
		"""
		转换field列表的真实值到差值
		"""
		last_field_id = 0
		for i in range(len(field_list)):
			item = field_list[i]
			item.setFieldIdDiff(item.getFieldId() - last_field_id)
			last_field_id = item.getFieldId()

	def convertIdToDiffForMethodList(self, method_list):
		"""
		转换method列表的真实值到差值
		"""
		last_method_id = 0
		for i in range(len(method_list)):
			item = method_list[i]
			item.setMethodIdDiff(item.getMethodId() - last_method_id)
			last_method_id = item.getMethodId()

	def getStaticFieldList(self):
		"""
		获取静态属性列表
		"""
		return self.static_field_list

	def getInstanceFieldList(self):
		"""
		获取实例属性列表
		"""		
		return self.instance_field_list

	def getDirectMethodList(self):
		"""
		获取直接方法列表
		"""
		return self.direct_method_list

	def getVirtualMethodList(self):
		"""
		获取虚方法列表
		"""
		return self.virtual_method_list

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = '{\n'

		string += 'static_field_size: %.4d\n' % self.static_field_size
		if self.static_field_size > 0:
			string += '    [\n'
			for item in self.static_field_list:
				string += ' ' * 8 + item.tostring() + '\n'
			string += '    ]\n'

		string += 'instance_field_size: %.4d\n' % self.instance_field_size
		if self.instance_field_size > 0:
			string += '    [\n'
			for item in self.instance_field_list:
				string += ' ' * 8 + item.tostring() + '\n'
			string += '    ]\n'

		string += 'direct_method_size: %.4d\n' % self.direct_method_size
		if self.direct_method_size > 0:
			string += '    [\n'
			for item in self.direct_method_list:
				string += ' ' * 8 + item.tostring() + '\n'
			string += '    ]\n'

		string += 'virtual_method_size: %.4d\n' % self.virtual_method_size
		if self.virtual_method_size > 0:
			string += '    [\n'
			for item in self.virtual_method_list:
				string += ' ' * 8 + item.tostring() + '\n'
			string += '    ]\n'

		string += '}\n'

		return string