# -- coding: utf-8 --

from item_base import *

class TypeListItem(BaseItem):
	"""
	section子结构: 类型列表项
	"""

	@classmethod
	def create(cls):
		"""
		创建子项
		"""
		return TypeListItem(createBytes(0x04))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(TypeListItem, self).__init__(bytes)

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
			item = TypeListItemData(bytes[off:off+0x02])

			# 添加数据列表
			self.item_list.append(item)

			# 偏移量增加
			off += 0x02

		# 四字节对齐
		if off % 0x04 != 0:
			off += 0x02

		# 重新调整字节数组的大小
		self.setBytes(bytes[0x00:off])


	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		# 检测尺寸变化
		self.item_size = len(self.item_list)
		new_size = 0x04 + self.item_size * 0x02
		if new_size % 0x04 != 0:    # 四字节对齐
			new_size += 0x02

		# print 'type_list_item new_size: %.4d cur_size: %.4d' % (new_size, self.getBytesSize())

		if self.getBytesSize() != new_size:
			self.setBytes(createBytes(new_size))

		bytes = self.getBytes()
		zerosBytes(bytes)

		# 记录尺寸
		bytes[0x00:0x04] = convertIntToBytes(self.item_size)

		# 循环拷贝列表数据
		off = 0x04
		for item in self.item_list:
			bytes[off:off+0x02] = item.bytes
			off += 0x02

	def getItemDataList(self):
		"""
		获取子项的数据列表，每一项代表一个类型
		"""
		return self.item_list

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = 'type_list_item_size: %d\n' % self.item_size
		for item in self.item_list:
			string += item.tostring() + '\n'

		return string
