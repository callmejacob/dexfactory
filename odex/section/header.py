# -- coding: utf-8 --

from tool import *

class OdexHeader(object):
	"""
	头部结构，固定大小0x28
	struct header {
		u1 magic[8];     // 魔数，必须为'dey\n036\n'
		u4 dex_off;      // dex段的字节偏移量
		u4 dex_size;     // dex段的字节长度
		u4 deps_off;     // deps段的字节偏移量
		u4 deps_size;    // deps段的字节长度
		u4 opt_off;      // opt段的字节偏移量
		u4 opt_size;     // opt段的字节长度
		u4 flags;        // 标志位
		u4 checksum;     // 总checksum
	}
	"""

	def __init__(self, bytes):

		self.magic        =    bytes[0x00:0x08]
		self.dex_off      =    convertBytesToInt(bytes[0x08:0x0c])
		self.dex_size     =    convertBytesToInt(bytes[0x0c:0x10])
		self.deps_off     =    convertBytesToInt(bytes[0x10:0x14])
		self.deps_size    =    convertBytesToInt(bytes[0x14:0x18])
		self.opt_off      =    convertBytesToInt(bytes[0x18:0x1c])
		self.opt_size     =    convertBytesToInt(bytes[0x1c:0x20])
		self.flags        =    convertBytesToInt(bytes[0x20:0x24])
		self.checksum     =    convertBytesToInt(bytes[0x24:0x28])

		self.bytes = bytes[0x00:0x28]

	def getBytesSize(self):
		return len(self.bytes)

	def tostring(self):
		string = 'header: {\n'

		string += ' ' * 4 + 'magic:        [%s]\n' % convertBytesToHexStr(self.magic)
		string += ' ' * 4 + 'dex_off:      %.4x\n' % self.dex_off
		string += ' ' * 4 + 'dex_size:     %.4x\n' % self.dex_size
		string += ' ' * 4 + 'deps_off:     %.4x\n' % self.deps_off
		string += ' ' * 4 + 'deps_size:    %.4x\n' % self.deps_size
		string += ' ' * 4 + 'opt_off:      %.4x\n' % self.opt_off
		string += ' ' * 4 + 'opt_size:     %.4x\n' % self.opt_size
		string += ' ' * 4 + 'flags:        %.4x\n' % self.flags
		string += ' ' * 4 + 'checksum:     %.4x\n' % self.checksum

		string += '}\n'

		return string
