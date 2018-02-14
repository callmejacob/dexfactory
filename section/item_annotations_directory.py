# -- coding: utf-8 --

from item_base import *

class AnnotationsDirectoryItem(BaseItem):
	"""
	section子结构: annotations_directory_item
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return AnnotationsDirectoryItem(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(AnnotationsDirectoryItem, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.getBytes()

		off = 0x00

		self.class_annotations_off        =    convertBytesToInt(bytes[off:off+0x04])
		self.class_annotations_id         =    -1
		self.class_annotations_item       =    None
		off += 0x04

		self.fields_size                  =    convertBytesToInt(bytes[off:off+0x04])
		off += 0x04

		self.annotated_methods_size       =    convertBytesToInt(bytes[off:off+0x04])
		off += 0x04

		self.annotated_parameters_size    =    convertBytesToInt(bytes[off:off+0x04])
		off += 0x04

		self.field_annotations = []
		for i in range(self.fields_size):
			item = FieldAnnotationData(bytes[off:])
			self.field_annotations.append(item)
			off += item.getBytesSize()

		self.method_annotations = []
		for i in range(self.annotated_methods_size):
			item = MethodAnnotationData(bytes[off:])
			self.method_annotations.append(item)
			off += item.getBytesSize()

		self.parameter_annotations = []
		for i in range(self.annotated_parameters_size):
			item = ParameterAnnotationData(bytes[off:])
			self.parameter_annotations.append(item)
			off += item.getBytesSize()

		# 重新调整字节数组的大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		# 重新调整大小
		self.fields_size = len(self.field_annotations)
		self.annotated_methods_size = len(self.method_annotations)
		self.annotated_parameters_size = len(self.parameter_annotations)

		new_size = 0x04 * 4
		for item in self.field_annotations:
			new_size += item.getBytesSize()
		for item in self.method_annotations:
			new_size += item.getBytesSize()
		for item in self.parameter_annotations:
			new_size += item.getBytesSize()

		if self.getBytesSize() != new_size:
			self.setBytes(createBytes(new_size))

		# 编码
		off = 0x00

		bytes[off:off+0x04]    =    convertIntToBytes(self.class_annotations_off)
		off += 0x04

		bytes[off:off+0x04]    =    convertIntToBytes(self.fields_size)
		off += 0x04

		bytes[off:off+0x04]    =    convertIntToBytes(self.annotated_methods_size)
		off += 0x04

		bytes[off:off+0x04]    =    convertIntToBytes(self.annotated_parameters_size)
		off += 0x04

		for item in self.field_annotations:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

		for item in self.method_annotations:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

		for item in self.parameter_annotations:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		self.class_annotations_id = context.getSectionItemIdByOff(TYPE_ANNOTATION_SET_ITEM, self.class_annotations_off)

		for item in self.field_annotations:
			item.convertOffToId(context)

		for item in self.method_annotations:
			item.convertOffToId(context)

		for item in self.parameter_annotations:
			item.convertOffToId(context)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		self.class_annotations_off = context.getSectionItemOffById(TYPE_ANNOTATION_SET_ITEM, self.class_annotations_id)

		for item in self.field_annotations:
			item.convertIdToOff(context)

		for item in self.method_annotations:
			item.convertIdToOff(context)

		for item in self.parameter_annotations:
			item.convertIdToOff(context)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		self.class_annotations_item = context.getSectionItemById(TYPE_ANNOTATION_SET_ITEM, self.class_annotations_id)

		for item in self.field_annotations:
			item.convertIdToItem(context)

		for item in self.method_annotations:
			item.convertIdToItem(context)

		for item in self.parameter_annotations:
			item.convertIdToItem(context)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		self.class_annotations_id = context.getSectionIdByItem(TYPE_ANNOTATION_SET_ITEM, self.class_annotations_item)

		for item in self.field_annotations:
			item.convertItemToId(context)

		for item in self.method_annotations:
			item.convertItemToId(context)

		for item in self.parameter_annotations:
			item.convertItemToId(context)

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = '{\n'
		string += 'class_annotations: [%.4x %.4d]\n' % (self.class_annotations_off, self.class_annotations_id)

		string += 'field_annotations_size: %.4d\n' % self.fields_size
		if self.fields_size > 0:
			print '    [\n'
			for item in self.field_annotations:
				string += ' ' * 8 + item.tostring() + '\n'
			print '    ]\n'

		string += 'method_annotations_size: %.4d\n' % self.annotated_methods_size
		if self.annotated_methods_size > 0:
			print '    [\n'
			for item in self.method_annotations:
				string += ' ' * 8 + item.tostring() + '\n'
			print '    ]\n'

		string += 'parameter_annotations_size: %.4d\n' % self.annotated_parameters_size
		if self.annotated_parameters_size > 0:
			print '    [\n'
			for item in self.parameter_annotations:
				string += ' ' * 8 + item.tostring() + '\n'
			print '    ]\n'

		string += '}\n'

		return string