# -- coding: utf-8 --

from section_base import *

class AnnotationItemSection(BaseSection):
	"""
	section: annotation_item
	"""

	def __init__(self, context, bytes, size, off):
		"""
		初始化
		context:    上下文信息
		bytes:      原始字节数组
		size:       子项总个数
		off:        字节数组偏移
		"""
		super(AnnotationItemSection, self).__init__(context, TYPE_ANNOTATION_ITEM, bytes[off:], size)

	def getItemDesc(self, index):
		"""
		获取子项的字符串描述
		index: 索引
		"""
		if index < self.item_size:
			item = self.item_list[index]

			string = '{\n'

			string += 'visibility: %s\n' % annotation_item_visibility_desc_map[item.visibility]

			# annotation
			annotation = item.annotation
			string += 'type: %s\n' % self.getContextDesc(TYPE_TYPE_ID_ITEM, annotation.type_id)
			string += 'element_size: %.4d\n' % annotation.item_size
			if annotation.item_size > 0:
				string += '    [\n'
				for element in annotation.item_list:
					element_string  = '%s:' % self.getContextDesc(TYPE_STRING_DATA_ITEM, element.name_id)

					element_value = element.value
					if element_value.value_type == ENCODED_VALUE_INT:
						value = convertBytesToInt(element_value.value.getBytes())
						element_string += ' %.4x' % value
					elif element_value.value_type == ENCODED_VALUE_STRING:
						string_id = convertBytesToInt(element_value.value.getBytes())
						element_string += ' %s' % self.getContextDesc(TYPE_STRING_DATA_ITEM, string_id)
					elif element_value.value_type == ENCODED_VALUE_TYPE:
						type_id = convertBytesToInt(element_value.value.getBytes())
						element_string += ' %s' % self.getContextDesc(TYPE_TYPE_ID_ITEM, type_id)
					else:
						 element_string += ' <%s>' % element.value.tostring()
					string += '        %s\n' % element_string
				string += '    ]\n'

			string += '}\n'
			
			return string

		return '%.4d' % index	