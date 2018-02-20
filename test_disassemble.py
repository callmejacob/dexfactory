# -- coding: utf-8 --

from dex import *
from disassemble import *

dex_path = './data/classes.dex'
dex = DexInfo(dex_path)
context = dex.context

######################################################################
'''
反汇编
'''
code_item_section = context.getSection(TYPE_CODE_ITEM)

# 反汇编
for item in code_item_section.item_list:
	print '[', convertBytesToHexStr(item.insns), ']'
	insns = Insns(item.insns)
	print insns.tostring(context)

# 将反汇编解析类挂接到context中
context.setInsnsClass(Insns)
print code_item_section.tostring()

######################################################################
