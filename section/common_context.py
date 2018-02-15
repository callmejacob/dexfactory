# -- coding: utf-8 --

from common_type import *

class Context(object):
	"""
	上下文信息，记录所有的section列表信息
	"""

	def __init__(self):
		self.string_list = None
		self.type_list = None
		self.proto_list = None

		self.section_map = {}
		for section_type in type_list:
			self.section_map[section_type] = None

		# 反汇编的类，外部可以绑定
		self.insns_class = None

	def getSectionList(self):
		"""
		获取section列表
		"""
		section_list = []

		map_item_list_section = self.getSection(TYPE_MAP_LIST)
		if map_item_list_section:
			for map_item in map_item_list_section.getItemDataList():
				section_type = map_item.getSectionType()
				section = self.section_map[section_type]
				if section:
					section_list.append(section)
				else:
					print 'not support [type %.4x]' % section_type
					
		return section_list

	def setSection(self, section_type, section_obj):
		"""
		设置section
		section_type:    section类型
		section_obj:     section对象
		"""
		self.section_map[section_type] = section_obj

	def getSection(self, section_type):
		"""
		获取section
		"""
		return self.section_map[section_type]

	def getSectionItemDesc(self, section_type, index):
		"""
		获取描述
		section_type:    section类型
		index:           section中子项列表的项索引
		"""
		section = self.getSection(section_type)
		if section:
			return section.getItemDesc(index)

		return '%.4d' % index

	def getSectionOff(self, section_type):
		map_item_list_section = self.getSection(TYPE_MAP_LIST)
		if map_item_list_section:
			for map_item in map_item_list_section.getItemDataList():
				map_item_type = map_item.getSectionType()
				if map_item_type == section_type:
					return map_item.getSectionOff()

		return -1

	def getSectionItemIdByOff(self, section_type, off):
		section_off = self.getSectionOff(section_type)

		if section_off == -1 or off < section_off:
			return -1

		section = self.getSection(section_type)
		if section:
			return section.getIdByOff(off - section_off)

		return -1

	def getSectionItemOffById(self, section_type, id):
		section_off = self.getSectionOff(section_type)
		if section_off == -1 or id == -1:
			return 0

		section = self.getSection(section_type)
		if section:
			return section_off + section.getOffById(id)

		return 0

	def getSectionItemById(self, section_type, id):
		section = self.getSection(section_type)
		if section:
			return section.getItemById(id)
		return None

	def getSectionIdByItem(self, section_type, item):
		section = self.getSection(section_type)
		if section:
			return section.getIdByItem(item)
		return -1

	def setInsnsClass(self, insns_class):
		"""
		设置反汇编的解析类
		insns_class:    反汇编的解析类
		"""
		self.insns_class = insns_class

	def getInsnsClass(self):
		"""
		获取反汇编的解析类
		"""
		return self.insns_class

