# -- coding: utf-8 --

import numpy as np

'''
字节数组操作
'''

def createBytes(size):
	"""
	创建字节数组
	size: 需要创建的字节数组大小
	"""
	return np.zeros(size).astype(np.ubyte)

def zerosBytes(bytes):
	"""
	将字节数组全部填充为0
	"""
	for i in range(len(bytes)):
		bytes[i] = 0



'''
转换字节数组到其它类型
'''

def convertBytesToInt(bytes):
	"""
	转换字节数组到整数
	bytes: 字节数组
	"""
	if len(bytes) < 4:
		value = 0
		for i in range(len(bytes)):
			value |= (bytes[i] << i*8)
		return value
	return (bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24))

def convertBytesToShort(bytes):
	"""
	转换字节数组到short类型
	bytes: 字节数组
	"""
	return (bytes[0] | (bytes[1] << 8))

def convertBytesToHexStr(data_bytes):
	"""
	转换字节数组到一个16进制字符串
	data_bytes: 字节数组
	"""
	data_str = []
	for i in range(0, len(data_bytes), 1):
		data_str.append('%.2x' % data_bytes[i])
	return ' '.join(data_str)

def convertUleb128BytesToInt(bytes): 
	"""
	转换字节数组到一个整型，这个字节数组是uleb128格式的
	"""
	# 计算终止位置（最高位是0）
	for last in range(5):
		if (bytes[last] & 0x80 == 0):
			break

	value = 0
	for i in range(last+1):
		value |= (bytes[i] & 0x7f) << i*7

	return value, last+1

def convertSleb128BytesToInt(bytes): 
	"""
	转换字节数组到一个整型，这个字节数组是uleb128格式的
	"""
	# 计算终止位置（最高位是0）
	for last in range(5):
		if (bytes[last] & 0x80 == 0):
			break

	value = 0
	for i in range(last+1):
		value |= (bytes[i] & 0x7f) << i*7

	return value, last+1


'''
转换其它类型到字节数组
'''
def convertIntToBytes(data):
	"""
	转换整数到字节数组
	data: 整数
	"""
	byte1 = data & 0xff
	byte2 = (data >> 8) & 0xff
	byte3 = (data >> 16) & 0xff
	byte4 = (data >> 24) & 0xff
	return [byte1, byte2, byte3, byte4]

def convertShortToBytes(data):
	"""
	转换short到字节数组
	data: short
	"""
	byte1 = data & 0xff
	byte2 = (data >> 8) & 0xff
	return [byte1, byte2]

def convertHexStrToBytes(hex_str):
	"""
	将一个16进制字符串转换到字节数组
	"""
	print 'hex_str:', hex_str
	return bytearray.fromhex(hex_str)

def convertStringToBytes(string):
	"""
	将一个字符串转换为字节数组
	"""
	return np.fromstring(string, dtype=np.byte)

def convertIntToUleb128Bytes(value): 
	"""
	转换一个整型到字节数组，这个字节数组是uleb128格式的
	"""
	bytes = createBytes(5)

	for i in range(5):
		bytes[i] = (value >> 7*i) & 0x7f

	# 倒着数，第一个不为0的位置就是last
	for last in range(len(bytes), 0, -1):
		if bytes[last-1] != 0:
			break

	for i in range(last-1):
		bytes[i] |= 0x80

	return bytes[0x00:last], last

def convertIntToSleb128Bytes(value): 
	"""
	转换一个整型到字节数组，这个字节数组是uleb128格式的
	"""
	bytes = createBytes(5)

	for i in range(5):
		bytes[i] = (value >> 7*i) & 0x7f

	# 倒着数，第一个不为0的位置就是last
	for last in range(len(bytes), 0, -1):
		if bytes[last-1] != 0:
			break

	for i in range(last-1):
		bytes[i] |= 0x80
		# print i

	return bytes[0x00:last], last


'''
打印方法
'''

def printSigAndChecksum(tag, sig, checksum):
	"""
	打印sig和checksum
	tag: 提示说明
	sig: sig
	checksum: checksum
	"""
	print '-*-' * 20
	print tag
	print 'sig: ', convertBytesToHexStr(sig)
	print 'checksum: ', convertBytesToHexStr(checksum)
	print '-*-' * 20, '\n'

def printHexArray(hex_list):
	"""
	打印十六进制数组的数组
	hex_list: 一个十六进制数组的数组
	"""
	for item in hex_list:
		print convertBytesToHexStr(item)



'''
对比方法
'''

def diffBytes(bytes1, bytes2):
	if len(bytes1) != len(bytes2):
		return False

	bytes_len = len(bytes1)
	for i in range(bytes_len):
		if bytes1[i] != bytes2[i]:
			return False

	return True