# -- coding: utf-8 --

from section import *

def cmpStringItem(item1, item2):
	if item1.string_data < item2.string_data:
		return -1
	elif item1.string_data > item2.string_data:
		return 1
	else:
		return 0

def modifyString(context):
	dst_string = 'yes you are!'

	string_id_section = context.getSection(TYPE_STRING_ID_ITEM)
	string_list_section = context.getSection(TYPE_STRING_DATA_ITEM)

	string_list = string_list_section.item_list

	# 记录原有列表
	src_string_list = []
	for item in string_list:
		src_string_list.append(item)

	# 修改某项
	modify_string_id = 58
	string_item = string_list[modify_string_id]
	print 'modify %s to %s' % (string_item.tostring(), dst_string)
	string_item.setString(dst_string)

	# 排序
	# string_list_section.sortItemList()
