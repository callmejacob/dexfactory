# -- coding: utf-8 --

from data_base import *


class AnnotationSetItemItemOffData(BaseData):
	"""
	注解列表中的子类型结构数据
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return AnnotationSetItemItemOffData(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(AnnotationSetItemItemOffData, self).__init__(bytes[0x00:0x04])

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		self.annotation_off = convertBytesToInt(bytes[0x00:0x04])

		self.annotation_id = -1
		self.annotation_item = None

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

		bytes[0x00:0x04] = convertIntToBytes(self.annotation_off)

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		self.annotation_id = context.getSectionItemIdByOff(TYPE_ANNOTATION_ITEM, self.annotation_off)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		self.annotation_off = context.getSectionItemOffById(TYPE_ANNOTATION_ITEM, self.annotation_id)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		self.annotation_item = context.getSectionItemById(TYPE_ANNOTATION_ITEM, self.annotation_id)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		self.annotation_id = context.getSectionIdByItem(TYPE_ANNOTATION_ITEM, self.annotation_item)

	def getAnnotationOff(self):
		"""
		获取注解信息偏移
		"""
		return self.annotation_off

	def setAnnotationannotation_offOff(self, annotation_off):
		"""
		设置注解信息偏移
		annotation_off:    注解信息偏移
		"""
		self.annotation_off = annotation_off
		self.encode()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		return 'annotation: [%.4x %.4d]' % (self.annotation_off, self.annotation_id)