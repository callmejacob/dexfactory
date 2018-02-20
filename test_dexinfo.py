# -- coding: utf-8 --

from dex import *
from test_modify import *

dex_path = './data/classes.dex'
dex = DexInfo(dex_path)

######################################################################
'''
修改区域
'''
print '-*-' * 30
print 'modify string {'

modifyString(dex.getContext())

print '}'
print '-*-' * 30

######################################################################

dex.encode()
dex.save('classes_new.dex')