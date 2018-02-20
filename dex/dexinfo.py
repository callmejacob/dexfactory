# -- coding: utf-8 --

import numpy as np
import hashlib
import zlib

from section import *

class DexInfo(object):
	"""
	dex信息
	"""

	def __init__(self, dex_path, dex_bytes = None):
		"""
		初始化
		dex_path: dex的文件路径

		self.dex_bytes:  dex的字节数组
		self.header:     头部信息的字节数组
		"""
		# 记录文件路径
		self.dex_path = dex_path

		# 获取dex的字节数组
		if dex_bytes is None:
			self.dex_bytes = np.fromfile(dex_path, dtype=np.ubyte)
		else:
			self.dex_bytes = dex_bytes

		# context
		self.context = Context()

		# 解码section列表
		self.decode()

	def decode(self):
		"""
		解码所有的section列表
		"""
		# 1. 获取头信息
		header = HeaderSection(self.context, self.dex_bytes, 1, 0).getItem(0)

		# 2. 获取map列表
		map_item_list = MapItemListSection(self.context, self.dex_bytes, 1, header.map_off)

		# 3. 解析所有的section字段
		for item in map_item_list.getItemDataList():
			section_type = item.getSectionType()
			section_item_size = item.getSectionItemSize()
			section_off = item.getSectionOff()

			section_class = section_class_map[section_type]
			if section_class:
				# print section_class
				section = section_class(self.context, self.dex_bytes, section_item_size, section_off)

		# 4. 转换[off ---> id]
		self.convertOffToIdForAllSections()

		# 5. 转换[id ---> item]
		self.convertIdToItemForAllSections()

		# 6. 记录头部信息
		self.header_section = self.context.getSection(TYPE_HEADER_ITEM)
		self.header = self.header_section.getItem(0)

	def encode(self):
		"""
		编码所有的section列表
		"""
		# 1. 重新编码所有的section
		self.encodeAllSections()

		# 2. 重新计算section偏移，并更新到map_list和header两个section中
		self.genAllSectionsOffAndSize()

		# 3. 转换[item ---> id]
		self.convertItemToIdForAllSections()

		# 4. 转换[id ---> off]
		self.convertIdToOffForAllSections()

		# 5. 重新编码调整过的section，并拷贝到字节数组中
		self.encodeAllSections()
		self.copyAllSections()

		# 6. 重新计算sig和checksum信息
		self.recalSigAndChecksum()

	def encodeAllSections(self):
		"""
		编码所有的section列表
		"""
		section_list = self.context.getSectionList()

		# 记录原有的hex信息
		src_hex_list = []
		for section in section_list:
			src_hex_list.append(section.tohexstring())

		# 列表重新编码
		for section in section_list:
			section.encode()

		section_list = self.context.getSectionList()

		# 记录原有的hex信息
		dst_hex_list = []
		for section in section_list:
			dst_hex_list.append(section.tohexstring())

		# 对比
		# string = 'encode_all_sections diff {\n'

		# string += 'len: %r\n' % (len(src_hex_list) == len(dst_hex_list))
		# for i in range(len(src_hex_list)):
		# 	src_hex_bytes = src_hex_list[i]
		# 	dst_hex_bytes = dst_hex_list[i]
		# 	section = section_list[i]
		# 	section_desc = type_desc_map[section.section_type]
		# 	diff_result = diffBytes(src_hex_bytes, dst_hex_bytes)
			
		# 	string += '-' * 100 + '\n'
		# 	string += '%s: %r\n' % (section_desc, diff_result)
		# 	if True:
		# 		string += 'src: [%s]\n\n' % src_hex_bytes
		# 		string += 'dst: [%s]\n' % dst_hex_bytes
		# 	string += '-' * 100 + '\n'

		# string += '}\n'

		# print string

	def genAllSectionsOffAndSize(self):
		"""
		更新所有section的偏移和大小
		"""
		map_list_section = self.context.getSection(TYPE_MAP_LIST)
		header = self.header

		section_list = self.context.getSectionList()

		section_size_off_map = {}
		for section_type in type_list:
			section_size_off_map[section_type] = None

		# 计算section偏移
		section_off = 0
		for section in section_list:
			section_size_off_map[section.section_type] = [section.getItemSize(), section_off]
			# print '%.4x: [%.4x %.4x %.4d]   (%s)' % (section.section_type, section.getItemSize(), section_off, section.getBytesSize(), type_desc_map[section.section_type])
			# print 'pre  section_off: %.4x bytes_size: %.4d' % (section_off, section.getBytesSize())
			section_off += section.getBytesSize()
			# print 'next section_off: %.4x bytes_size: %.4d' % (section_off, section.getBytesSize())

		file_size = section_off
		if file_size % 0x02 != 0: 	# 确保数据区尺寸为偶数
			file_size += 0x01
		# print 'file_size: %.4x' % file_size

		# 更新到map_list_section中
		for map_item in map_list_section.getItemDataList():
			section_type = map_item.getSectionType()

			section_item_size, section_item_off = section_size_off_map[section_type]

			map_item.setSectionItemSize(section_item_size)
			map_item.setSectionOff(section_item_off)

		map_list_section.encode()

		# 更新到头部信息
		# print 'Before gen header:\n', header.tostring()

		header.setFileSize(file_size)

		section_item_size, section_off = section_size_off_map[TYPE_MAP_LIST]
		header.setMapOff(section_off)

		section_item_size, section_off = section_size_off_map[TYPE_STRING_ID_ITEM]
		header.setStringIdInfo(section_item_size, section_off)

		section_item_size, section_off = section_size_off_map[TYPE_TYPE_ID_ITEM]
		header.setTypeIdInfo(section_item_size, section_off)

		section_item_size, section_off = section_size_off_map[TYPE_PROTO_ID_ITEM]
		header.setProtoIdInfo(section_item_size, section_off)

		section_item_size, section_off = section_size_off_map[TYPE_FIELD_ID_ITEM]
		header.setFieldIdInfo(section_item_size, section_off)

		section_item_size, section_off = section_size_off_map[TYPE_METHOD_ID_ITEM]
		header.setMethodInfo(section_item_size, section_off)

		section_item_size, class_def_section_off = section_size_off_map[TYPE_CLASS_DEF_ITEM]
		header.setClassDefInfo(section_item_size, class_def_section_off)

		class_def_section = self.context.getSection(TYPE_CLASS_DEF_ITEM)
		data_area_off = class_def_section_off + class_def_section.getBytesSize()
		data_area_size = file_size - data_area_off
		header.setDataInfo(data_area_size, data_area_off)

		# print 'After gen header:\n', header.tostring()

	def copyAllSections(self):
		"""
		拷贝所有的section
		"""
		section_list = self.context.getSectionList()
		header = self.header

		# 重新调整字节数组大小
		bytes = createBytes(header.file_size)

		# 依次拷贝section
		section_off = 0
		for section in section_list:
			section_bytes_size = section.getBytesSize()
			bytes[section_off:section_off+section_bytes_size] = section.getBytes()
			section_off += section_bytes_size

		# 比较字节数组
		# diff_result = diffBytes(self.dex_bytes, bytes)
		# print 'after copy_all_sections:\n', diff_result

		# 重新调整dex的字节数组
		self.dex_bytes = bytes

	def printAllSections(self):
		"""
		打印所有的section列表
		"""
		section_list = self.context.getSectionList()
		for section in section_list:
			if section:
				print section.tostring()

	def printSection(self, section_type):
		''' 打印指定类型的section '''
		section = self.context.getSection(section_type)
		if section:
			print section.tostring()

	def convertOffToIdForAllSections(self):
		''' 转换文件偏移量到相关的id '''
		section_list = self.context.getSectionList()
		for section in section_list:
			section.convertOffToId()

	def convertIdToOffForAllSections(self):
		''' 转换id到相关的文件偏移量 '''
		section_list = self.context.getSectionList()
		for section in section_list:
			section.convertIdToOff()

	def convertIdToItemForAllSections(self):
		''' 转换id到item对象 '''
		section_list = self.context.getSectionList()
		for section in section_list:
			section.convertIdToItem()

	def convertItemToIdForAllSections(self):
		''' 转换item对象到id '''
		section_list = self.context.getSectionList()
		for section in section_list:
			section.convertItemToId()
			# if section.section_type == TYPE_PROTO_ID_ITEM:
			# 	print section.tostring()

	def getContext(self):
		"""
		获取上下文信息
		"""
		return self.context

	def save(self, dex_path=None):
		"""
		将字节数组保存到文件中
		"""
		if dex_path is None:
			dex_path = self.dex_path
		if not dex_path is None:
			self.dex_bytes.tofile(dex_path)

	def recalSigAndChecksum(self):
		"""
		计算sig和checksum信息
		"""
		dex_bytes = self.dex_bytes
		dex_size = len(dex_bytes)

		# 计算sig
		sig = hashlib.sha1(dex_bytes[32:dex_size]).hexdigest()
		self.header.setSignature(bytearray.fromhex(sig))

		# 更新sig到dex_bytes中
		self.header_section.encode()
		dex_bytes[0x00:self.header_section.getBytesSize()] = self.header_section.getBytes()

		# 计算checksum (checksum的计算包含了sig，所以需要sig先写入)
		checksum = zlib.adler32(dex_bytes[12:dex_size])
		self.header.setChecksum(convertIntToBytes(checksum))

		# 更新checksum到dex_bytes中
		self.header_section.encode()
		dex_bytes[0x00:self.header_section.getBytesSize()] = self.header_section.getBytes()

	def tostring(self):
		string = ''
		section_list = self.context.getSectionList()
		for section in section_list:
			if section:
				string += section.tostring()
		return string
