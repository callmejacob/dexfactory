# -- coding: utf-8 --

from item_base import *

class HeaderItem(BaseItem):
	"""
	section子结构: 头部信息项
	"""

	@classmethod
	def create(cls):
		"""
		创建项
		"""
		return HeaderItem(createBytes(0x70))

	def __init__(self, bytes):
		"""
		初始化
		bytes:    字节数组
		"""
		super(HeaderItem, self).__init__(bytes[0x00:0x70])

		self.decode()

	def decode(self):
		"""
		从字节数组中解析变量
		"""
		bytes = self.getBytes()

		self.magic           = bytes[0x00:0x08]
		self.checksum        = bytes[0x08:0x0C]
		self.signature       = bytes[0x0C:0x20]
		self.file_size       = convertBytesToInt(bytes[0x20:0x24])
		self.header_size     = convertBytesToInt(bytes[0x24:0x28])
		self.endian_tag      = convertBytesToInt(bytes[0x28:0x2C])
		self.link_size       = convertBytesToInt(bytes[0x2C:0x30])
		self.link_off        = convertBytesToInt(bytes[0x30:0x34])
		self.map_off         = convertBytesToInt(bytes[0x34:0x38])
		self.string_ids_size = convertBytesToInt(bytes[0x38:0x3C])		
		self.string_ids_off  = convertBytesToInt(bytes[0x3C:0x40])
		self.type_ids_size   = convertBytesToInt(bytes[0x40:0x44])
		self.type_ids_off    = convertBytesToInt(bytes[0x44:0x48])
		self.proto_ids_size  = convertBytesToInt(bytes[0x48:0x4C])
		self.proto_ids_off   = convertBytesToInt(bytes[0x4C:0x50])
		self.field_ids_size  = convertBytesToInt(bytes[0x50:0x54])
		self.field_ids_off   = convertBytesToInt(bytes[0x54:0x58])
		self.method_ids_size = convertBytesToInt(bytes[0x58:0x5C])
		self.method_ids_off  = convertBytesToInt(bytes[0x5C:0x60])
		self.class_defs_size = convertBytesToInt(bytes[0x60:0x64])
		self.class_defs_off  = convertBytesToInt(bytes[0x64:0x68])
		self.data_size       = convertBytesToInt(bytes[0x68:0x6C])
		self.data_off		 = convertBytesToInt(bytes[0x6C:0x70])		

		# 调整字节数组尺寸
		self.setBytes(bytes[0x00:0x70])

	def encode(self):
		"""
		将变量重新写入到字节数组中
		"""
		bytes = self.getBytes()

		bytes[0x00:0x08]  = self.magic
		bytes[0x08:0x0C]  = self.checksum
		bytes[0x0C:0x20]  = self.signature
		bytes[0x20:0x24]  = convertIntToBytes(self.file_size)
		bytes[0x24:0x28]  = convertIntToBytes(self.header_size)
		bytes[0x28:0x2C]  = convertIntToBytes(self.endian_tag)
		bytes[0x2C:0x30]  = convertIntToBytes(self.link_size)
		bytes[0x30:0x34]  = convertIntToBytes(self.link_off)
		bytes[0x34:0x38]  = convertIntToBytes(self.map_off)
		bytes[0x38:0x3C]  = convertIntToBytes(self.string_ids_size)
		bytes[0x3C:0x40]  = convertIntToBytes(self.string_ids_off)
		bytes[0x40:0x44]  = convertIntToBytes(self.type_ids_size)
		bytes[0x44:0x48]  = convertIntToBytes(self.type_ids_off)
		bytes[0x48:0x4C]  = convertIntToBytes(self.proto_ids_size)
		bytes[0x4C:0x50]  = convertIntToBytes(self.proto_ids_off)
		bytes[0x50:0x54]  = convertIntToBytes(self.field_ids_size)
		bytes[0x54:0x58]  = convertIntToBytes(self.field_ids_off)
		bytes[0x58:0x5C]  = convertIntToBytes(self.method_ids_size)
		bytes[0x5C:0x60]  = convertIntToBytes(self.method_ids_off)
		bytes[0x60:0x64]  = convertIntToBytes(self.class_defs_size)
		bytes[0x64:0x68]  = convertIntToBytes(self.class_defs_off)
		bytes[0x68:0x6C]  = convertIntToBytes(self.data_size)
		bytes[0x6C:0x70]  = convertIntToBytes(self.data_off)

	def setChecksum(self, checksum):
		self.checksum = checksum
		self.encode()

	def setSignature(self, signature):
		self.signature = signature
		self.encode()

	def setFileSize(self, file_size):
		self.file_size = file_size
		self.encode()

	def setLinkInfo(size, off):
		self.link_size = size
		self.link_off = off
		self.encode()

	def setMapOff(self, off):
		self.map_off = off
		self.encode()

	def setStringIdInfo(self, size, off):
		self.string_ids_size = size
		self.string_ids_off = off
		self.encode()

	def setTypeIdInfo(self, size, off):
		self.type_ids_size = size
		self.type_ids_off = off
		self.encode()

	def setProtoIdInfo(self, size, off):
		self.proto_ids_size = size
		self.proto_ids_off = off
		self.encode()

	def setFieldIdInfo(self, size, off):
		self.field_ids_size = size
		self.field_ids_off = off
		self.encode()

	def setMethodInfo(self, size, off):
		self.method_ids_size = size
		self.method_ids_off = off
		self.encode()

	def setClassDefInfo(self, size, off):
		self.class_defs_size = size
		self.class_defs_off = off
		self.encode()

	def setDataInfo(self, size, off):
		self.data_size = size
		self.data_off = off
		self.encode()

	def tostring(self):
		"""
		转化为可打印的字符串
		"""
		magic_hexstr = convertBytesToHexStr(self.magic)
		checksum_hexstr = convertBytesToHexStr(self.checksum)
		signature_hexstr = convertBytesToHexStr(self.signature)
		string = '{\nmagic: %s\nchecksum: %s\nsignature: %s\nfile_size: %x\nheader_size: %x \
				\nendian_tag: %x\nlink_size: %x\nlink_off: %x\nmap_off: %x\nstring_id_size: %x\nstring_id_off: %x \
				\ntype_ids_size: %x\ntype_ids_off: %x\nproto_ids_size: %x\nproto_ids_off: %x \
				\nfield_ids_size: %x\nfield_ids_off: %x\nmethod_ids_size: %x\nmethod_ids_off: %x \
				\nclass_defs_size: %x\nclass_def_off: %x\ndata_size: %x\ndata_off: %x\n}' % ( \
					magic_hexstr, checksum_hexstr, signature_hexstr, self.file_size, self.header_size, \
					self.endian_tag, self.link_size, self.link_off, self.map_off, self.proto_ids_size, self.proto_ids_off, \
					self.type_ids_size, self.type_ids_off, self.proto_ids_size, self.proto_ids_off, \
					self.field_ids_size, self.field_ids_off, self.method_ids_size, self.method_ids_off, \
					self.class_defs_size, self.class_defs_off, self.data_size, self.data_off)
		return string