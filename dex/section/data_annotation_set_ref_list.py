# -- coding: utf-8 --

from data_base import *


class AnnotationSefRefListItemData(BaseData):
	"""
	注解引用列表中的子类型结构数据
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return AnnotationSefRefListItemData(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(AnnotationSefRefListItemData, self).__init__(bytes[0x00:0x04])

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		self.annotations_off = convertBytesToInt(bytes[0x00:0x04])

		self.annotations_id = -1
		self.annotations_item = None

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

		bytes[0x00:0x04] = convertIntToBytes(self.annotations_off)

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		self.annotations_id = context.getSectionItemIdByOff(TYPE_ANNOTATION_SET_ITEM, self.annotations_off)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		self.annotations_off = context.getSectionItemOffById(TYPE_ANNOTATION_SET_ITEM, self.annotations_id)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		self.annotations_item = context.getSectionItemById(TYPE_ANNOTATION_SET_ITEM, self.annotations_id)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		self.annotations_id = context.getSectionIdByItem(TYPE_ANNOTATION_SET_ITEM, self.annotations_item)

	def getAnnotationsOff(self):
		"""
		获取注解信息偏移
		"""
		return self.annotations_off

	def setAnnotationsOff(self, annotations_off):
		"""
		设置注解信息偏移
		annotations_off:    注解信息偏移
		"""
		self.annotations_off = annotations_off
		self.encode()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		return 'annotations_off: %.4x, annotations_id: %.4d' % (self.annotations_off, self.annotations_id)

