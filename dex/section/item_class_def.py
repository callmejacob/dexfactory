# -- coding: utf-8 --

from item_base import *

class ClassDefItem(BaseItem):
	"""
	section子结构: 类定义
	"""

	@classmethod
  	def create(cls):
  		"""
  		创建一个新项
  		"""
  		return ClassDefItem(createBytes(0x20))

	def __init__(self, bytes):
		"""
		初始化
		bytes:  原始字节数组
		"""
		super(ClassDefItem, self).__init__(bytes[0x00:0x20])

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.class_id            =    convertBytesToInt(bytes[0x00:0x04])
		self.access_flags        =    convertBytesToInt(bytes[0x04:0x08])
		self.super_class_id      =    convertBytesToInt(bytes[0x08:0x0c])
		self.interface_off       =    convertBytesToInt(bytes[0x0c:0x10])
		self.source_file_id      =    convertBytesToInt(bytes[0x10:0x14])
		self.annotation_off      =    convertBytesToInt(bytes[0x14:0x18])
		self.class_data_off      =    convertBytesToInt(bytes[0x18:0x1c])
		self.static_value_off    =    convertBytesToInt(bytes[0x1c:0x20])
		
		self.interface_id        =    -1
		self.interface_item      =    None

		self.annotation_id       =    -1
		self.annotation_item     =    None

		self.class_data_id       =    -1
		self.class_data_item     =    None

		self.static_value_id     =    -1
		self.static_value_item   =    None

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:0x20])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		bytes[0x00:0x04]    =    convertIntToBytes(self.class_id)
		bytes[0x04:0x08]    =    convertIntToBytes(self.access_flags)
		bytes[0x08:0x0c]    =    convertIntToBytes(self.super_class_id)
		bytes[0x0c:0x10]    =    convertIntToBytes(self.interface_off)
		bytes[0x10:0x14]    =    convertIntToBytes(self.source_file_id)
		bytes[0x14:0x18]    =    convertIntToBytes(self.annotation_off)
		bytes[0x18:0x1c]    =    convertIntToBytes(self.class_data_off)
		bytes[0x1c:0x20]    =    convertIntToBytes(self.static_value_off)

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		self.interface_id = context.getSectionItemIdByOff(TYPE_TYPE_LIST, self.interface_off)
		self.annotation_id = context.getSectionItemIdByOff(TYPE_ANNOTATIONS_DIRECTORY_ITEM, self.annotation_off)
		self.class_data_id = context.getSectionItemIdByOff(TYPE_CLASS_DATA_ITEM, self.class_data_off)
		self.static_value_id = context.getSectionItemIdByOff(TYPE_ENCODED_ARRAY_ITEM, self.static_value_off)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		self.interface_off = context.getSectionItemOffById(TYPE_TYPE_LIST, self.interface_id)
		self.annotation_off = context.getSectionItemOffById(TYPE_ANNOTATIONS_DIRECTORY_ITEM, self.annotation_id)
		self.class_data_off = context.getSectionItemOffById(TYPE_CLASS_DATA_ITEM, self.class_data_id)
		self.static_value_off = context.getSectionItemOffById(TYPE_ENCODED_ARRAY_ITEM, self.static_value_id)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		self.interface_item = context.getSectionItemById(TYPE_TYPE_LIST, self.interface_id)
		self.annotation_item = context.getSectionItemById(TYPE_ANNOTATIONS_DIRECTORY_ITEM, self.annotation_id)
		self.class_data_item = context.getSectionItemById(TYPE_CLASS_DATA_ITEM, self.class_data_id)
		self.static_value_item = context.getSectionItemById(TYPE_ENCODED_ARRAY_ITEM, self.static_value_id)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		self.interface_id = context.getSectionIdByItem(TYPE_TYPE_LIST, self.interface_item)
		self.annotation_id = context.getSectionIdByItem(TYPE_ANNOTATIONS_DIRECTORY_ITEM, self.annotation_item)
		self.class_data_id = context.getSectionIdByItem(TYPE_CLASS_DATA_ITEM, self.class_data_item)
		self.static_value_id = context.getSectionIdByItem(TYPE_ENCODED_ARRAY_ITEM, self.static_value_item)

	def getClassId(self):
		"""
		获取类id
		"""
		return self.class_id

	def getAccessFlags(self):
		"""
		获取类id
		"""
		return self.access_flags

	def getSuperClassId(self):
		"""
		获取类id
		"""
		return self.super_class_id

	def getInterfaceOff(self):
		"""
		获取接口偏移值
		"""
		return self.interface_off

	def getSourceFileId(self):
		"""
		获取源文件id
		"""
		return self.source_file_id

	def getAnnotationOff(self):
		"""
		获取注解偏移量
		"""
		return self.annotation_off

	def getClassDataOff(self):
		"""
		获取类数据偏移量
		"""
		return self.class_data_off

	def getStaticValueOff(self):
		"""
		获取静态数据偏移量
		"""
		return self.static_value_off

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''
		string += 'class: %.4d' % self.class_id
		string += ', access_flags: %.4x' % self.access_flags
		string += ', super_class: %.4d' % self.super_class_id
		string += ', interface: [%.4x %.4d]' % (self.interface_off, self.interface_id)
		string += ', source_file: %.4d' % self.source_file_id
		string += ', annotation: [%.4x %.4d]' % (self.annotation_off, self.annotation_id)
		string += ', class_data: [%.4d %.4d]' % (self.class_data_off, self.class_data_id)
		string += ', static_value: [%.4x %.4d]' % (self.static_value_off, self.static_value_id)
		return string
