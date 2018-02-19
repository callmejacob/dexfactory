# -- coding: utf-8 --

from odexinfo import *
from dexinfo import *

odex_path = './data/classes.odex'

odex = OdexInfo(odex_path, DexInfo)
print odex.tostring()