# -- coding: utf-8 --

from item_base import *

class AnnotationSetItemItem(BaseItem):
	"""
	section子结构: 注解列表
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return AnnotationSetItemItem(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(AnnotationSetItemItem, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.getBytes()

		self.item_size = convertBytesToInt(bytes[0x00:0x04])
		self.item_list = []

		off = 0x04
		for i in range(self.item_size):
			# 解码子项数据
			item = AnnotationSetItemItemOffData(bytes[off:off+0x04])

			# 添加数据列表
			self.item_list.append(item)

			# 偏移量增加
			off += 0x04

		# 重新调整字节数组的大小
		self.setBytes(bytes[0x00:off])


	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		# 子项列表编码
		for item in self.item_list:
			item.encode()

		# 检测尺寸变化
		self.item_size = len(self.item_list)

		new_size = 0x04 + self.item_size * 0x04
		if self.getBytesSize() != new_size:
			self.setBytes(createBytes(new_size))

		# 编码
		bytes = self.getBytes()

		# 记录尺寸
		bytes[0x00:0x04] = convertIntToBytes(self.item_size)

		# 循环拷贝列表数据
		off = 0x04
		for item in self.item_list:
			bytes[off:off+0x04] = item.bytes
			off += 0x04

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		for item in self.item_list:
			item.convertOffToId(context)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		for item in self.item_list:
			item.convertIdToOff(context)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		for item in self.item_list:
			item.convertIdToItem(context)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		for item in self.item_list:
			item.convertItemToId(context)

	def getItemDataList(self):
		"""
		获取子项的数据列表，每一项代表一个类型
		"""
		return self.item_list

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = '{\n'

		string += 'annotation_sef_item_item_size: %.4d\n' % self.item_size
		if self.item_size > 0:
			string += '    [\n'
			for item in self.item_list:
				string += ' ' * 8 + item.tostring() + '\n'
			string += '    ]\n'

		string += '}\n'

		return string	