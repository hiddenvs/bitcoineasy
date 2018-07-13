from hashlib import *

# Returns the ripemd160(sha256(data)), used a lot in Bitcoin
def hash160(data):
	rip = new('ripemd160')
	sha = new('sha256')
	sha.update(str(data).encode())
	print("sha256 : ", sha.hexdigest())
	rip.update(str(sha.hexdigest()).encode())
	return rip.hexdigest()
	
# Returns the sha256(sha256(data)), also used a lot
def double_sha256(data):
	h = sha256()
	h.update(str(data).encode())
	h.update(str(h.hexdigest()).encode())
	return h.hexdigest()
	
# Takes a number (hex or dec) and returns its base58_encoding
def base58_encode(data):
	alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	x = data % 58
	rest = data // 58
	if rest == 0:
		return alphabet[x]
	else:
		return base58_encode(rest) + alphabet[x]
		
#def base58_decode(data):

# Returns the base58check_encoded data, with prefix "version". <data> and <version> must be int !
def base58check_encode(data, version):
	payload = str('00').encode()+str(data).encode()
	checksum = double_sha256(str(version+data).encode())
	return base58_encode(version+data+int(checksum, 16))

#def base58check_decode(data):
