from random import randint
from math import *
from hashlib import *
from requests import get
from time import time

N = 1.158 * pow(10, 77)
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)

def gen_random():
	h = sha256()
	# 2 or 3 differents sources of entropy 
	h.update(str(randint(0, pow(2, 256))).encode())
	h.update(str(time()).encode())
	try:
		req = get("https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard")
		h.update(str(req.content).encode())
	except:
		pass
	finally:
		return int(h.hexdigest(), 16)

def gen_privkey():
	valid = False
	while not valid:
		k = gen_random()
		valid = 0 < k < N
	return k
	
def get_pubkey(privkey):
	pubkey = privkey * G
	return pubkey
	
print(get_pubkey(gen_privkey()))
