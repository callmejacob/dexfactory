# -- coding: utf-8 --

from insns_type import *


class InsnsItem(object):
	"""
	指令说明格式
	"""

	def __init__(self, bytes):
		self.bytes = bytes
		self.bytes_size = len(bytes)

		self.desc = None

		self.op = bytes[0]
		self.format_id = format_map[self.op]
		self.kind = kind_map[self.op]
		self.kind_x = None
		self.proto_x = None

		self.decode()

	def decode(self):
		"""
		解码
		"""
		bytes = self.bytes

		if self.format_id == '00x':
			self.bytes_size = 0x01
			self.desc = '%s'

		elif self.format_id == '10x':
			self.bytes_size = 0x01

			op = bytes[0x00]

			self.desc = '%s' % op_map[op]

		elif self.format_id == '12x' or self.format_id == '11n':
			self.bytes_size = 0x02

			op = bytes[0x00]
			B = (bytes[0x01] >> 4) & 0x0f
			A = (bytes[0x01] >> 0) & 0x0f

			if self.format_id == '12x':
				self.desc = '%s v%d, v%d' % (op_map[op], A, B)
			elif self.format_id == '11n':
				self.desc = '%s v%d, #+%x' % (op_map[op], A, B)

		elif self.format_id == '11x' or self.format_id == '10t':
			self.bytes_size = 0x02

			op = bytes[0x00]
			AA = bytes[0x01]

			if self.format_id == '11x':
				self.desc = '%s v%d' % (op_map[op], AA)
			elif self.format_id == '10t':
				self.desc = '%s +v%d' % (op_map[op], AA)

		elif self.format_id == '20t':
			self.bytes_size = 0x04

			op = bytes[0x00]
			AAAA = (bytes[0x02] << 0) | (bytes[0x03] << 8)

			self.desc = '%s +%.4x' % (op_map[op], AAAA)

		elif self.format_id == '20bc':
			self.bytes_size = 0x04

			op = bytes[0x00]
			AA = bytes[0x01]
			BBBB = (bytes[0x02] << 0) | (bytes[0x03] << 8)

			self.desc = '%s %.2d, %s' % (op_map[op], AA, '%s')
			self.kind_x = BBBB

		elif self.format_id == '22x' \
			or self.format_id == '21t' \
			or self.format_id == '21s' \
			or self.format_id == '21h' \
			or self.format_id == '21c':

			self.bytes_size = 0x04

			op = bytes[0x00]
			AA = bytes[0x01]
			BBBB = (bytes[0x02] << 0) | (bytes[0x03] << 8)

			if self.format_id == '22x':
				self.desc = '%s v%d, v%d' % (op_map[op], AA, BBBB)
			elif self.format_id == '21t':
				self.desc = '%s v%d, +%.4x' % (op_map[op], AA, BBBB)
			elif self.format_id == '21s':
				self.desc = '%s v%d, #+%.4x' % (op_map[op], AA, BBBB)
			elif self.format_id == '21h':
				self.desc = '%s v%d, #+%.4x0000' % (op_map[op], AA, BBBB)
			elif self.format_id == '21c':
				self.desc = '%s v%d, %s' % (op_map[op], AA, '%s')
				self.kind_x = BBBB

		elif self.format_id == '23x' or self.format_id == '22b':
			self.bytes_size = 0x04

			op = bytes[0x00]
			AA = bytes[0x01]
			BB = bytes[0x02]
			CC = bytes[0x03]

			if self.format_id == '23x':
				self.desc = '%s v%d, v%d, v%x' % (op_map[op], AA, BB, CC)
			elif self.format_id == '22b':
				self.desc = '%s v%d, v%d, #+%.2x' % (op_map[op], AA, BB, CC)

		elif self.format_id == '22t' \
			or self.format_id == '22s' \
			or self.format_id == '22c' \
			or self.format_id == '22cs':

			self.bytes_size = 0x04

			op = bytes[0x00]
			A = (bytes[0x01] >> 0) & 0x0f
			B = (bytes[0x01] >> 4) & 0x0f
			CCCC = (bytes[0x02] << 0) | (bytes[0x03] << 8)

			if self.format_id == '22t':
				self.desc = '%s v%d, v%d, +%.4x' % (op_map[op], A, B, CCCC)
			elif self.format_id == '22s':
				self.desc = '%s v%d, v%d, #+%.4x' % (op_map[op], A, B, CCCC)
			elif self.format_id == '22c':
				self.desc = '%s v%d, v%d, %s' % (op_map[op], A, B, '%s')
				self.kind_x = CCCC
			elif self.format_id == '22cs':
				self.desc = '%s v%d, v%d, %s' % (op_map[op], A, B, '%s')
				self.kind_x = CCCC

		elif self.format_id == '30t':
			self.bytes_size = 0x06

			op = bytes[0x00]
			AAAAAAAA = (bytes[0x02] << 0) | (bytes[0x03] << 8) | (bytes[0x04] << 16) | (bytes[0x05] << 24)

			self.desc = '%s +%.8x' % (op_map[op], AAAAAAAA)

		elif self.format_id == '32x':
			self.bytes_size = 0x06

			op = bytes[0x00]
			AAAA = (bytes[0x02] << 0) | (bytes[0x03] << 8)
			BBBB = (bytes[0x04] << 0) | (bytes[0x05] << 8)

			self.desc = '%s v%d, v%d' % (op_map[op], AAAA, BBBB)

		elif self.format_id == '31i' \
			or self.format_id == '31t' \
			or self.format_id == '31c':

			self.bytes_size = 0x06

			op = bytes[0x00]
			AA = bytes[0x01]
			BBBBBBBB = (bytes[0x02] << 0) | (bytes[0x03] << 8) | (bytes[0x04] << 16) | (bytes[0x05] << 24)

			if self.format_id == '31i':
				self.desc = '%s v%d, #+%.8x' % (op_map[op], AA, BBBBBBBB)
			elif self.format_id == '31t':
				self.desc = '%s v%d, +%.8x' % (op_map[op], AA, BBBBBBBB)
			elif self.format_id == '31c':
				self.desc = '%s v%d, %s' % (op_map[op], AA, '%s')
				self.kind_x = BBBBBBBB

		elif self.format_id == '35c' \
			or self.format_id == '35ms' \
			or self.format_id == '35mi':
			self.bytes_size = 0x06

			op = bytes[0x00]
			A = (bytes[0x01] >> 4) & 0x0f
			G = (bytes[0x01] >> 0) & 0x0f
			BBBB = (bytes[0x02] << 0) | (bytes[0x03] << 8)
			C = (bytes[0x04] >> 0) & 0x0f
			D = (bytes[0x04] >> 4) & 0x0f
			E = (bytes[0x05] >> 0) & 0x0f
			F = (bytes[0x05] >> 4) & 0x0f

			if A == 0:
				self.desc = '%s {}, %s' % (op_map[op], '%s')
				self.kind_x = BBBB
			elif A == 1:
				self.desc = '%s {v%d}, %s' % (op_map[op], C, '%s')
				self.kind_x = BBBB
			elif A == 2:
				self.desc = '%s {v%d, v%d}, %s' % (op_map[op], C, D, '%s')
				self.kind_x = BBBB
			elif A == 3:
				self.desc = '%s {v%d, v%d, v%d}, %s' % (op_map[op], C, D, E, '%s')
				self.kind_x = BBBB
			elif A == 4:
				self.desc = '%s {v%d, v%d, v%d, v%d}, %s' % (op_map[op], C, D, E, F, '%s')
				self.kind_x = BBBB
			elif A == 5:
				self.desc = '%s {v%d, v%d, v%d, v%d, v%d}, %s' % (op_map[op], C, D, E, F, G, '%s')
				self.kind_x = BBBB

		elif self.format_id == '3rc' \
			or self.format_id == '3rms' \
			or self.format_id == '3rmi':
			self.bytes_size = 0x06

			op = bytes[0x00]
			AA = bytes[0x01]
			BBBB = (bytes[0x02] << 0) | (bytes[0x03] << 8)
			CCCC = (bytes[0x04] << 0) | (bytes[0x05] << 8)
			NNNN = CCCC + AA - 1

			self.desc = '%s {v%d ... v%d} %s' % (op_map[op], CCCC, NNNN, '%s')
			self.kind_x = BBBB

		elif self.format_id == '45cc':
			self.bytes_size = 0x08

			op = bytes[0x00]
			G = (bytes[0x01] >> 0) & 0x0f
			A = (bytes[0x01] >> 4) & 0x0f

			BBBB = (bytes[0x02] << 0) | (bytes[0x03] << 8)
			C = (bytes[0x04] >> 0) & 0x0f
			D = (bytes[0x04] >> 4) & 0x0f
			E = (bytes[0x05] >> 0) & 0x0f
			F = (bytes[0x05] >> 4) & 0x0f
			HHHH = (bytes[0x06] << 0) | (bytes[0x07] << 8)

			if A == 1:
				self.desc = '%s {v%d}, %s, %s' % (op_map[op], C, '%s', '%s')
				self.kind_x = BBBB
				self.proto_x = HHHH
			elif A == 2:
				self.desc = '%s {v%d, v%d}, %s, %s' % (op_map[op], C, D, '%s', '%s')
				self.kind_x = BBBB
				self.proto_x = HHHH
			elif A == 3:
				self.desc = '%s {v%d, v%d, v%d}, %s, %s' % (op_map[op], C, D, E, '%s', '%s')
				self.kind_x = BBBB
				self.proto_x = HHHH
			elif A == 4:
				self.desc = '%s {v%d, v%d, v%d, v%d}, %s, %s' % (op_map[op], C, D, E, F, '%s', '%s')
				self.kind_x = BBBB
				self.proto_x = HHHH
			elif A == 5:
				self.desc = '%s {v%d, v%d, v%d, v%d, v%d}, %s, %s' % (op_map[op], C, D, E, F, G, '%s', '%s')
				self.kind_x = BBBB
				self.proto_x = HHHH

		elif self.format_id == '4rcc':
			self.bytes_size = 0x08

			op = bytes[0x00]
			AA = bytes[0x01]
			BBBB = (bytes[0x02] << 0) | (bytes[0x03] << 8)
			CCCC = (bytes[0x04] << 0) | (bytes[0x05] << 8)
			HHHH = (bytes[0x06] << 0) | (bytes[0x07] << 8)
			NNNN = CCCC + AA - 1

			self.desc = '%s> {v%d ... v%d}, %s, %s' % (op_map[op], CCCC, NNNN, '%s', '%s')
			self.kind_x = BBBB
			self.proto_x = HHHH

		elif self.format_id == '51l':
			self.bytes_size = 0x0a

			op = bytes[0x00]
			AA = bytes[0x01]
			BBBBBBBBBBBBBBBB =  (bytes[0x02] <<  0) | (bytes[0x03] <<  8)
			BBBBBBBBBBBBBBBB |= (bytes[0x04] << 16) | (bytes[0x05] << 24)
			BBBBBBBBBBBBBBBB |= (bytes[0x06] << 32) | (bytes[0x07] << 40)
			BBBBBBBBBBBBBBBB |= (bytes[0x04] << 48) | (bytes[0x09] << 56)

			self.desc = '%s v%d, #+%.16x' % (op_map[op], AA, BBBBBBBBBBBBBBBB)

		self.bytes = bytes[0x00:self.bytes_size]

	def getKindInfo(self):
		"""
		获取kind相关的信息
		"""
		return self.kind, self.kind_x, self.proto_x

	def format(self, kind_desc = None, proto_desc = None):
		"""
		格式化
		kind_desc:    kind相关的描述
		proto_desc:   proto相关的描述
		"""
		if not self.desc is None:
			if not kind_desc is None and not proto_desc is None:
				return self.desc % (kind_desc, proto_desc)
			elif not kind_desc is None:
				return self.desc % kind_desc
			else:
				return self.desc
		return None

	def tostring(self):
		"""
		转换成字符串
		"""
		string = ''

		kind_desc = None
		proto_desc = None
		if not self.kind_x is None and not self.proto_x is None:
			kind_desc = '%s@%.4x' % (self.kind, self.kind_x)
			proto_desc = '%s@%.4x' % (KIND_PROTO, self.proto_x)
		elif not self.kind_x is None:
			kind_desc = '%s@%.4x' % (self.kind, self.kind_x)

		string += self.format(kind_desc, proto_desc)

		return string
