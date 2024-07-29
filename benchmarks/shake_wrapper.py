from hashlib import shake_128, shake_256

class ShakeStream:
	"""	
	Written by David Buchanan
	
    Taken from:
	https://github.com/pyca/cryptography/issues/9185#issuecomment-1868518432
	"""
	def __init__(self, digestfn) -> None:
		# digestfn is anything we can call repeatedly with different lengths
		self.digest = digestfn
		self.buf = self.digest(32) # arbitrary starting length
		self.offset = 0
	
	def read(self, n: int) -> bytes:
		# double the buffer size until we have enough
		while self.offset + n > len(self.buf):
			self.buf = self.digest(len(self.buf) * 2)
		res = self.buf[self.offset:self.offset + n]
		self.offset += n
		return res
	
def shake_128_hashlib(absorb):
	return ShakeStream(shake_128(absorb).digest)

def shake_256_hashlib(absorb):
	return ShakeStream(shake_256(absorb).digest)
