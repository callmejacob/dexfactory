# -- coding: utf-8 --

from item_base import *

"""
annotation_item中的visibility的描述映射
"""
annotation_item_visibility_desc_map = {

	0x00        :        'VISIBILITY_BUILD',
	0x01        :        'VISIBILITY_RUNTIME',
	0x02        :        'VISIBILITY_SYSTEM',

}


class AnnotationItemItem(BaseItem):
	"""
	section子结构: annotation_item
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return AnnotationItemItem(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(AnnotationItemItem, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.getBytes()

		self.visibility = bytes[0x00]
		self.annotation = EncodedAnnotationData(bytes[0x01:])

		# 重新调整字节数组的大小
		new_size = 0x01 + self.annotation.getBytesSize()
		self.setBytes(bytes[0x00:new_size])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		# 检测尺寸变化
		new_size = 0x01 + self.annotation.getBytesSize()
		if self.getBytesSize() != new_size:
			self.setBytes(createBytes(new_size))

		# 编码
		bytes = self.getBytes()

		bytes[0x00] = self.visibility
		bytes[0x01:0x01+self.annotation.getBytesSize()] = self.annotation.getBytes()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = '{\n'

		string += 'visibility: %.1x\n' % self.visibility
		string += 'annotation: %s\n' % self.annotation.tostring()
		string += '}\n'

		return string	