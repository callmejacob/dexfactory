# -- coding: utf-8 --

from data import *

class BaseItem(BytesObject):
	"""
	基类，所有dex的section中各个子项的结构类都继承这个类
	"""

	def __init__(self, bytes):
		"""
		bytes: 原始字节数组
		"""
		super(BaseItem, self).__init__(bytes)

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		pass

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		pass

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		pass

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		pass