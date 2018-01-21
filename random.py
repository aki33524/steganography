from RC4 import RC4

class Random():
	def __init__(self, key):
		self.rc4 = RC4(key)

	def get_nbits(self, n):
		res = 0

		for i in range((n+7)//8):
			res = (res<<8) | self.rc4.rand()

		mask = 0
		for i in range(n):
			mask |= 1<<i

		return res & mask

	def randint(self, n):
		# return [0, n] randomly
		while True:
			x = self.get_nbits(n.bit_length())
			if x <= n:
				return x
