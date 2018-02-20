# -- coding: utf-8 --

from data_base import *


class TryItemData(BaseData):
	"""
	data: try_item
	"""

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(TryItemData, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		self.start_addr     =    convertBytesToInt(bytes[0x00:0x04])
		self.insn_count     =    convertBytesToShort(bytes[0x04:0x06])
		self.handler_off    =    convertBytesToShort(bytes[0x06:0x08])

		self.handler        =    -1

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:0x08])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.bytes

		bytes[0x00:0x04]    =    convertIntToBytes(self.start_addr)
		bytes[0x04:0x06]    =    convertShortToBytes(self.insn_count)
		bytes[0x06:0x08]    =    convertShortToBytes(self.handler_off)

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

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''

		string += 'start_addr: %.4d' % self.start_addr
		string += ' insn_count: %.4d' % self.insn_count
		string += ' handler_off: %.4d' % self.handler_off

		return string



class EncodedTypeAddrPairData(BaseData):
	"""
	data: encoded_type_addr_pair
	"""

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(EncodedTypeAddrPairData, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		off = 0

		self.type_idx, read_size    =    convertUleb128BytesToInt(bytes[off:])
		off += read_size

		self.addr, read_size        =    convertUleb128BytesToInt(bytes[off:])
		off += read_size

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		# 重新计算大小
		new_size = 0

		type_ids_bytes, type_ids_bytes_size = convertIntToUleb128Bytes(self.type_idx)
		new_size += type_ids_bytes_size

		addr_bytes, addr_bytes_size = convertIntToUleb128Bytes(self.addr)
		new_size += addr_bytes_size

		if self.getBytesSize() != new_size:
			self.setBytes(createBytes(new_size))

		# 编码
		bytes = self.bytes

		off = 0

		bytes[off:off+type_ids_bytes_size]    =    type_ids_bytes
		off += type_ids_bytes_size

		bytes[off:off+addr_bytes_size]        =    addr_bytes
		off += addr_bytes_size

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''

		string += 'type_idx: %.4d' % self.type_idx
		string += ' addr: %.4d' % self.addr

		return string



class EncodedCatchHandlerData(BaseData):
	"""
	data: encoded_catch_handler
	"""

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(EncodedCatchHandlerData, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		off = 0

		self.size, read_size = convertSleb128BytesToInt(bytes[off:])
		off += read_size

		self.handlers = []
		for i in range(abs(self.size)):
			item = EncodedTypeAddrPairData(bytes[off:])
			self.handlers.append(item)
			off += item.getBytesSize()

		self.catch_all_addr = 0
		if self.size <= 0:
			self.catch_all_addr, read_size = convertUleb128BytesToInt(bytes[off:])
			off += read_size

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		# 重新计算大小
		new_size = 0

		size_bytes, size_bytes_size = convertIntToSleb128Bytes(self.size)
		new_size += size_bytes_size

		for item in self.handlers:
			new_size += item.getBytesSize()

		if self.size <= 0:
			catch_all_addr_bytes, catch_all_addr_bytes_size = convertIntToSleb128Bytes(self.catch_all_addr)
			new_size += catch_all_addr_bytes_size

		if self.getBytesSize() != new_size:
			self.setBytes(createBytes(new_size))

		# 编码
		bytes = self.bytes

		off = 0

		bytes[off:off+size_bytes_size]    =    size_bytes
		off += size_bytes_size

		for item in self.handlers:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

		if self.size <= 0:
			bytes[off:off+catch_all_addr_bytes_size] = catch_all_addr_bytes
			off += catch_all_addr_bytes_size

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''

		string += 'size: %.4d\n' % self.size
		if abs(self.size) > 0:
			print '    [\n'
			for item in self.handlers:
				string += ' ' * 8 + item.tostring() + '\n'
			print '    ]\n'
		string += 'catch_all_addr: %.4d\n' % self.catch_all_addr

		return string



class EncodedCatchHandlerListData(BaseData):
	"""
	data: encoded_catch_handler_list
	"""

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(EncodedCatchHandlerListData, self).__init__(bytes)

		self.decode()

	def decode(self):
		"""
		解码字节数组
		"""
		bytes = self.bytes

		off = 0

		self.size, read_size = convertUleb128BytesToInt(bytes[off:])
		off += read_size

		self.list = []
		for i in range(self.size):
			item = EncodedCatchHandlerData(bytes[off:])
			self.list.append(item)
			off += item.getBytesSize()

		# 重新调整字节数组大小
		self.setBytes(bytes[0x00:off])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		# 重新计算大小
		new_size = 0

		size_bytes, size_bytes_size = convertIntToSleb128Bytes(self.size)
		new_size += size_bytes_size

		for item in self.list:
			new_size += item.getBytesSize()

		if self.getBytesSize() != new_size:
			self.setBytes(createBytes(new_size))

		# 编码
		bytes = self.bytes

		off = 0

		bytes[off:off+size_bytes_size]    =    size_bytes
		off += size_bytes_size

		for item in self.list:
			bytes[off:off+item.getBytesSize()] = item.getBytes()
			off += item.getBytesSize()

	def tostring(self):
		"""
		转换为可打印的字符串
		"""
		string = ''

		string += 'size: %.4d\n' % self.size
		if self.size > 0:
			print '    [\n'
			for item in self.list:
				string += ' ' * 8 + item.tostring() + '\n'
			print '    ]\n'

		return string
