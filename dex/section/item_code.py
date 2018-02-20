# -- coding: utf-8 --

from item_base import *

class CodeItem(BaseItem):
	"""
	section子结构: code_item
	"""

	@classmethod
  	def create(cls):
  		"""
  		创建一个新项
  		"""
  		return CodeItem(createBytes(0x10))

	def __init__(self, bytes):
		"""
		初始化
		bytes:  原始字节数组
		"""
		super(CodeItem, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.registers_size    =    convertBytesToShort(bytes[0x00:0x02])
		self.ins_size          =    convertBytesToShort(bytes[0x02:0x04])
		self.outs_size         =    convertBytesToShort(bytes[0x04:0x06])
		self.tries_size        =    convertBytesToShort(bytes[0x06:0x08])
		self.debug_info_off    =    convertBytesToInt(bytes[0x08:0x0c])
		self.insns_size        =    convertBytesToInt(bytes[0x0c:0x10])

		self.debug_info_id     =    -1
		self.debug_info_item   =    None

		off = 0x10

		self.insns = createBytes(self.insns_size*0x02)
		self.insns[0x00:self.insns_size*0x02] = bytes[off:off+self.insns_size*0x02]
		off += self.insns_size*0x02

		if self.tries_size > 0 and (self.insns_size & 0x01) == 0x01:
			off += 0x02

		self.tries = []
		if self.tries_size > 0:
			for i in range(self.tries_size):
				item = TryItemData(bytes[off:])
				self.tries.append(item)
				off += item.getBytesSize()

		self.handlers = None
		if self.tries_size > 0:
			self.handlers = EncodedCatchHandlerListData(bytes[off:])
			off += self.handlers.getBytesSize()

		# 四字节对齐
		if off % 0x04 != 0:
			off += 0x04 - (off % 0x04)

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		# 调整变量
		self.tries_size = len(self.tries)

		# 调整尺寸
		new_size = 0x10 + self.insns_size * 0x02

		if self.tries_size > 0 and (self.insns_size & 0x01) == 0x01:
			new_size += 0x02

		for item in self.tries:
			new_size += item.getBytesSize()

		if self.handlers:
			new_size += self.handlers.getBytesSize()

		if new_size % 0x04 != 0:
			new_size += 0x04 - (new_size % 0x04)

		if self.getBytesSize != new_size:
			self.setBytes(createBytes(new_size))
		else:
			# 考虑四字节对齐的影响
			zerosBytes(self.getBytes())

		# 编码
		bytes = self.getBytes()

		bytes[0x00:0x02]    =    convertShortToBytes(self.registers_size)
		bytes[0x02:0x04]    =    convertShortToBytes(self.ins_size)
		bytes[0x04:0x06]    =    convertShortToBytes(self.outs_size)
		bytes[0x06:0x08]    =    convertShortToBytes(self.tries_size)
		bytes[0x08:0x0c]    =    convertIntToBytes(self.debug_info_off)
		bytes[0x0c:0x10]    =    convertIntToBytes(self.insns_size)

		off = 0x10

		if self.insns_size > 0:
			bytes[off:off+self.insns_size*0x02] = self.insns[0x00:self.insns_size*0x02]
			off += self.insns_size*0x02

		if self.tries_size > 0 and (self.insns_size & 0x01) == 0x01:
			bytes[off+0x00] = 0
			bytes[off+0x01] = 0
			off += 0x02

		for item in self.tries:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

		if self.handlers:
			bytes[off:off+self.handlers.getBytesSize()] = self.handlers.getBytes()
			off += self.handlers.getBytesSize()

	def convertOffToId(self, context):
		''' 转换文件偏移量到相关的id '''
		self.debug_info_id = context.getSectionItemIdByOff(TYPE_DEBUG_INFO_ITEM, self.debug_info_off)

	def convertIdToOff(self, context):
		''' 转换id到相关的文件偏移量 '''
		self.debug_info_off = context.getSectionItemOffById(TYPE_DEBUG_INFO_ITEM, self.debug_info_id)

	def convertIdToItem(self, context):
		''' 转换id到item对象 '''
		self.debug_info_item = context.getSectionItemById(TYPE_DEBUG_INFO_ITEM, self.debug_info_id)

	def convertItemToId(self, context):
		''' 转换item对象到id '''
		self.debug_info_id = context.getSectionIdByItem(TYPE_DEBUG_INFO_ITEM, self.debug_info_item)

	def tostring(self, context = None):
		"""
		转换为可打印的字符串
		"""
		string = '{\n'
		string += 'registers_size:    %.4d\n' % self.registers_size
		string += 'ins_size:          %.4d\n' % self.ins_size
		string += 'outs_size:         %.4d\n' % self.outs_size
		string += 'tries_size:        %.4d\n' % self.tries_size
		string += 'debug_info:        [%.4x %.4d],\n' % (self.debug_info_off, self.debug_info_id)
		string += 'insns_size:        %.4d\n' % self.insns_size
		string += 'insns:             [%s]\n' % convertBytesToHexStr(self.insns)

		if not context is None:
			insns_class = context.getInsnsClass()
			if not insns_class is None:
				insns = insns_class(self.insns)
				string += '\ndisassemble: {\n'
				string += insns.tostring(context)
				string += '}\n\n'

		if self.tries_size > 0:
			string += 'tries_size:        %.4d\n' % self.tries_size
			string += '    [\n'
			for item in self.tries:
				string += ' '*8 + item.tostring() + '\n'
			string += '    ]\n'

		if self.handlers:
			string += 'handler: %s\n' + self.handlers.tostring()

		string += '}\n'

		return string
