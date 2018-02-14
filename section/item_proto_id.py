# -- coding: utf-8 --

from item_base import *

class ProtoIdItem(BaseItem):
	"""
	字符串项
	"""

	@classmethod
  	def create(cls):
  		"""
  		创建一个新项
  		"""
  		return ProtoIdItem(createBytes(0x0c))

	def __init__(self, bytes):
		"""
		初始化
		bytes:  原始字节数组
		"""
		super(ProtoIdItem, self).__init__(bytes[0x00:0x0c])

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.name_id =         convertBytesToInt(bytes[0x00:0x04])
		self.return_type_id =  convertBytesToInt(bytes[0x04:0x08])
		self.param_off =       convertBytesToInt(bytes[0x08:0x0c])

		self.param_id = -1
		self.param_item = None

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:0x0c])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		bytes[0x00:0x04] = convertIntToBytes(self.name_id)
		bytes[0x04:0x08] = convertIntToBytes(self.return_type_id)
		bytes[0x08:0x0c] = convertIntToBytes(self.param_off)

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		self.param_id = context.getSectionItemIdByOff(TYPE_TYPE_LIST, self.param_off)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		self.param_off = context.getSectionItemOffById(TYPE_TYPE_LIST, self.param_id)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		self.param_item = context.getSectionItemById(TYPE_TYPE_LIST, self.param_id)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		self.param_id = context.getSectionIdByItem(TYPE_TYPE_LIST, self.param_item)

	def getNameId(self):
		"""
		获取名称id
		"""
		return self.name_id

	def getReturnTypeId(self):
		"""
		获取返回类型id
		"""
		return self.return_type_id

	def getParamOff(self):
		"""
		获取参数列表的偏移数值
		"""
		return self.param_off

	def setNameId(self, name_id):
		"""
		设置名称id
		name_id: 名称id
		"""
		self.name_id = name_id
		self.encode()

	def setReturnTypeId(self, return_type_id):
		"""
		设置返回类型id
		return_type_id: 返回类型id
		"""
		self.return_type_id = return_type_id
		self.encode()

	def setParamOff(self, param_off):
		"""
		设置参数的偏移数值
		param_off: 参数列表的偏移数值
		"""
		self.param_off = param_off
		self.encode()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		return 'name_id: %.4d, return_type_id: %.4d, param: [%.4x %.4d]' % (self.name_id, self.return_type_id, self.param_off, self.param_id)
