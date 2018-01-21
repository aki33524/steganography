from struct import pack, unpack

IV_LENGTH = 16

def bytes_to_long(s):
	acc = 0
	length = len(s)
	if length % 4:
		extra = (4 - length % 4)
		s = b'\x00' * extra + s
		length = length + extra
	for i in range(0, length, 4):
		acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
	return acc

def long_to_bytes(n):
	s = b''
	while n > 0:
		s = pack('>B', n & 0xff) + s
		n = n >> 8
	return s