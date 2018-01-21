class RC4():
	def __init__(self, key):
		self.KSA(key)
		self.si = 0
		self.sj = 0

	def KSA(self, key):
		self.S = list(range(256))
		j = 0
		for i in range(256):
			j = (j + self.S[i] + key[i % len(key)]) % 256
			self.S[i], self.S[j] = self.S[j], self.S[i]

	def rand(self):
		self.si = (self.si + 1) % 256
		self.sj = (self.sj + self.S[self.si]) % 256
		self.S[self.si], self.S[self.sj] = self.S[self.sj], self.S[self.si]
		return self.S[(self.S[self.si] + self.S[self.sj]) % 256]

def encrypt(plaintext, key):
	rc4 = RC4(key)

	l = []
	for p in plaintext:
		s = rc4.rand()
		l.append(s^p)
	return bytes(l)