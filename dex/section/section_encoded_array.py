# -- coding: utf-8 --

from section_base import *

class EncodedArraySection(BaseSection):
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
		super(EncodedArraySection, self).__init__(context, TYPE_ENCODED_ARRAY_ITEM, bytes[off:], size)

	def getItemDesc(self, index):
		"""
		获取子项的字符串描述
		index: 索引
		"""
		if index < self.item_size:
			item = self.item_list[index]
			data = item.value

			string = '{\n'

			# data
			string += 'element_size: %.4d\n' % data.item_size
			if data.item_size > 0:
				string += '    [\n'
				for element_value in data.item_list:
					element_string  = ''

					if element_value.value_type == ENCODED_VALUE_INT:
						value = convertBytesToInt(element_value.value.getBytes())
						element_string += '%.4x' % value
					elif element_value.value_type == ENCODED_VALUE_STRING:
						string_id = convertBytesToInt(element_value.value.getBytes())
						element_string += '%s' % self.getContextDesc(TYPE_STRING_DATA_ITEM, string_id)
					elif element_value.value_type == ENCODED_VALUE_TYPE:
						type_id = convertBytesToInt(element_value.value.getBytes())
						element_string += '%s' % self.getContextDesc(TYPE_TYPE_ID_ITEM, type_id)
					elif element_value.value_type == ENCODED_VALUE_BOOLEAN:
						if element_value.value_arg == 0:
							element_string += 'false'
						else:
							element_string += 'true'
					else:
						 element_string += '<%s>' % element_value.tostring()
					string += '        %s\n' % element_string
				string += '    ]\n'

			string += '}\n'

			# 对照描述
			# string += '---> '
			# string += item.tostring()
			# string += '<---\n\n'
			
			return string

		return '%.4d' % index	