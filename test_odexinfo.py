# -- coding: utf-8 --

from odex import *
from dexinfo import *

odex_path = './data/classes.odex'

odex = OdexInfo(odex_path, DexInfo)
print odex.tostring()


"""
系统odex的测试
"""

# odex.dex.printAllSections()
# odex.dex.save('./data/classes_restore.dex')


# def scrapy(path_base):
# 	odex_path = '%s.odex' % path_base
# 	odex = OdexInfo(odex_path)
# 	print odex.tostring()

# 	dex_path = '%s.dex' % path_base
# 	odex.saveDex(dex_path)

# 	dex = DexInfo(dex_path)
# 	dex.printSection(TYPE_METHOD_ID_ITEM)
# 	dex.printSection(TYPE_TYPE_ID_ITEM)

# 	method_id_section = dex.context.getSection(TYPE_METHOD_ID_ITEM)
# 	print method_id_section.getItemDesc(0x00b2)

# 	string_data_section = dex.context.getSection(TYPE_STRING_DATA_ITEM)
# 	if 'Landroid/app/Activity;' in string_data_section.item_list:
# 		print 'find it !!!'


"""
抓取framework.odex
"""
# scrapy('./data/framework')


"""
抓取core.odex
"""
# scrapy('./data/core')

"""
抓取ext.odex
"""
# scrapy('./data/ext')

"""
抓取am.odex
"""
# scrapy('./data/am')

"""
抓取policy
"""
# scrapy('./data/android.policy')

"""
抓取pm
"""
# scrapy('./data/pm')

"""
抓取content
"""
# scrapy('./data/content')