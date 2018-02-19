# -- coding: utf-8 --

from tool import *
import hashlib

class OdexDepsItem(object):
	"""
	依赖目录的子项结构
	struct deps_item {
		u4        name_size;          // 依赖名称占有的字节数
		u1        name[name_size];    // 依赖名称
		u1[20]    sha1;               // 依赖库文件的sha1数值
	}
	"""

	def __init__(self, bytes):

		off = 0x00

		self.name_size = convertBytesToInt(bytes[off:off+0x04])
		off += 0x04

		self.name = bytes[off:off+self.name_size]
		off += self.name_size

		self.sha1 = bytes[off:off+0x14]
		off += 0x14

		self.bytes = bytes[0x00:off]

	def getNameString(self):
		return convertBytesToStr(self.name)

	def tostring(self):
		string = ''
		string += 'name: ' + convertBytesToStr(self.name) + '\n'
		string += 'sha1: ' + convertBytesToHexStr(self.sha1) + '\n'
		return string

class OdexDeps(object):
	"""
	依赖目录结构
	struct deps {
		u4           mod_when;                      // 修改时间戳
		u4           dex_crc;                       // 原dex文件的crc值 
		u4           dalvik_vm_build;               // 虚拟机版本
		u4           deps_items_num;                // 依赖项总个数
		deps_item    deps_items[deps_items_num];    // 依赖项列表
	}
	"""

	def __init__(self, bytes):
		self.mod_when = convertBytesToInt(bytes[0x00:0x04])
		self.dex_crc = convertBytesToInt(bytes[0x04:0x08])
		self.dalvik_vm_build = convertBytesToInt(bytes[0x08:0x0c])
		self.deps_items_num = convertBytesToInt(bytes[0x0c:0x10])
		self.deps_items = []

		off = 0x10
		for i in range(self.deps_items_num):
			item = OdexDepsItem(bytes[off:])
			self.deps_items.append(item)
			off += len(item.bytes)

		self.bytes = bytes[0x00:off]

	def tostring(self):
		string = 'deps: {\n'

		string += ' ' * 4 + 'mod_when:           %.4x\n' % self.mod_when
		string += ' ' * 4 + 'dex_crc:            %.4x\n' % self.dex_crc
		string += ' ' * 4 + 'dalvik_vm_build:    %.4x\n' % self.dalvik_vm_build
		string += ' ' * 4 + 'deps_items_num:     %.4x\n' % self.deps_items_num

		if self.deps_items_num > 0:
			string += ' ' * 4 + '[\n'
			for item in self.deps_items:
				string += ' ' * 8 + item.getNameString() + '\n'
			string += ' ' * 4 + ']\n'

		string += '}\n'

		return string