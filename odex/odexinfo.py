# -- coding: utf-8 --

import numpy as np

from section import *

class OdexInfo(object):
	"""
	odex信息
	"""

	def __init__(self, odex_path, dex_class = None):
		"""
		初始化
		odex_path:    odex的文件路径
		"""
		self.bytes = np.fromfile(odex_path, dtype=np.ubyte)

		# header
		self.header = OdexHeader(self.bytes)
		self.header_off = 0x00
		self.header_size = self.header.getBytesSize()

		# dex
		self.dex_off = self.header.dex_off
		self.dex_size = self.header.dex_size
		self.dex = None
		if not dex_class is None:
			self.dex = dex_class(None, self.bytes[self.dex_off:self.dex_off+self.dex_size])

		# deps
		self.deps_off = self.header.deps_off
		self.deps_size = self.header.deps_size
		self.deps = OdexDeps(self.bytes[self.deps_off:self.deps_off+self.deps_size])

		# opt
		self.opt_off = self.header.opt_off
		self.opt_size = self.header.opt_size
		self.opt = OdexOpt(self.bytes[self.opt_off:self.opt_off+self.opt_size])

	def saveDex(self, dex_path):
		if not dex_path is None:
			dex_bytes = self.bytes[self.dex_off:self.dex_off+self.dex_size]
			dex_bytes.tofile(dex_path)

	def tostring(self):
		string = ''
		string += self.header.tostring()
		if not self.dex is None:
			string += self.dex.tostring()
		string += self.deps.tostring()
		if not self.opt is None:
			string += self.opt.tostring()
		return string