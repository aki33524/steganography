import os
from struct import pack, unpack
from PIL import Image
from RC4 import encrypt
from random import Random
from misc import long_to_bytes, bytes_to_long, IV_LENGTH

class Stegano():
	def __init__(self, filename, key):
		self.image = Image.open(filename)
		assert self.image.format == 'PNG' and self.image.mode == 'RGB'
		
		self.rand = Random(key)
		self.used = set()

	def get_rand_pixel(self):
		W, H = self.image.size
		while True:
			x = (self.rand.randint(H-1), self.rand.randint(W-1), self.rand.randint(2))
			if x not in self.used:
				self.used.add(x)
				return x

	def embed(self, s):
		# embed s
		si = bytes_to_long(s)

		for i in range(len(s)*8):
			h, w, c = self.get_rand_pixel()
			color = list(self.image.getpixel((w, h)))
			color[c] = (color[c]&0xfe)+ ((si>>(len(s)*8-i-1))&1)
			self.image.putpixel((w, h), tuple(color))

	def extract(self, n):
		# extract n bytes
		res = 0
		for _ in range(n*8):
			h, w, c = self.get_rand_pixel()
			res = (res<<1) | (self.image.getpixel((w, h))[c]&1)
		return long_to_bytes(res)

def embed(key, cover_filename, message_filename, embedded_filename):
	stegano = Stegano(cover_filename, key)
	
	with open(message_filename, 'rb') as f:
		plaintext = f.read()

	iv = os.urandom(IV_LENGTH)
	s = iv + encrypt(pack('<I', len(plaintext))+plaintext, iv+key)
	stegano.embed(s)

	stegano.image.save(embedded_filename)


def extract(key, embedded_filename, extracted_filename):
	stegano = Stegano(embedded_filename, key)
	iv = stegano.extract(IV_LENGTH)
	nkey = iv+key

	esize = stegano.extract(4)
	size = unpack('<I', encrypt(esize, nkey))[0]

	with open(extracted_filename, 'wb') as f:
		f.write(encrypt(esize+stegano.extract(size), nkey)[4:])

if __name__ == '__main__':
	key = b'passphrase'

	message_filename = 'data/embedded'
	extracted_filename = 'data/extracted'
	cover_filename 	= 'img/cover.png'
	embedded_filename = 'img/coverd.png'

	embed(key, cover_filename, message_filename, embedded_filename)
	extract(key, embedded_filename, extracted_filename)

	with open(message_filename, 'rb') as f:
		message = f.read()
	
	with open(extracted_filename, 'rb') as f:
		extracted = f.read()

	assert message == extracted
