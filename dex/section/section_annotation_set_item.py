# -- coding: utf-8 --

from section_base import *

class AnnotationSetItemSection(BaseSection):
	"""
	section: annotation_set_item
	"""

	def __init__(self, context, bytes, size, off):
		"""
		初始化
		context:    上下文信息
		bytes:      原始字节数组
		size:       子项总个数
		off:        字节数组偏移
		"""
		super(AnnotationSetItemSection, self).__init__(context, TYPE_ANNOTATION_SET_ITEM, bytes[off:], size)

