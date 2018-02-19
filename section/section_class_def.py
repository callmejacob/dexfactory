# -- coding: utf-8 --

from section_base import *

class ClassDefListSection(BaseSection):
	"""
	section: class def列表
	"""

	def __init__(self, context, bytes, size, off):
		"""
		初始化
		context:    上下文信息
		bytes:      原始字节数组
		size:       项列表的总个数
		off:        字节数组偏移
		"""
		super(ClassDefListSection, self).__init__(context, TYPE_CLASS_DEF_ITEM, bytes[off:], size)

	def getItemDesc(self, index):
		"""
		获取proto id的字符串描述
		index: 索引
		"""
		if index >= self.item_size:
			return ''

		item = self.item_list[index]

		class_string = self.getContextDesc(TYPE_TYPE_ID_ITEM, item.getClassId())
		super_class_string = self.getContextDesc(TYPE_TYPE_ID_ITEM, item.getSuperClassId())
		source_file_string = self.getContextDesc(TYPE_STRING_DATA_ITEM, item.getSourceFileId())

		string = ''

		# string += 'access: %.4x\n' % item.access_flags
		string += '[%s] extends [%s] in [%s]' % (class_string, super_class_string, source_file_string)
		string += ' %s' % self.getContextDesc(TYPE_CLASS_DATA_ITEM, item.class_data_id)

		return string