from py_ecc import secp256k1 # https://github.com/ethereum/py_ecc/blob/master/py_ecc/secp256k1/secp256k1.py
from utils import *

N = 1.158 * pow(10, 77) # Max private key value


# Generates a pseudo-random private key. Returns int.
def gen_privkey(compressed=True):
    valid = False
    while not valid:
        k = gen_random()
        valid = 0 < k < N
    if compressed:
        k = int.from_bytes(k.to_bytes(sizeof(k), 'big')+0x01.to_bytes(1, 'big'), 'big')
    return k # type : int


# Takes a private key as int or bytes and returns its derived public key as a tuple of int
def get_pubkey_points(privkey):
    if isinstance(privkey, int):
        if sizeof(privkey) == 33: # If compressed
            privkey = int.from_bytes(privkey.to_bytes(33, 'big')[:32], 'big')
        (x, y) = secp256k1.privtopub(privkey.to_bytes(sizeof(privkey), 'big'))
    elif isinstance(privkey, bytes):
        if len(privkey) == 33: # If compressed
            privkey = privkey[:32]
        (x, y) = secp256k1.privtopub(privkey)
    else:
        raise ValueError("privkey must be int or bytes")
    return (x, y)


# Takes a private key as int or bytes and returns its derived public key as bytes
def get_pubkey(privkey):
    # Checking key format
    if isinstance(privkey, int):
        privkey = privkey.to_bytes(sizeof(privkey), 'big')
    elif not isinstance(privkey, bytes) and not isinstance(privkey, int):
        raise ValueError("Private key must be passed as int or bytes")
    # Checking key compression
    compressed = len(privkey) == 33
    if compressed:
        privkey = privkey[:32]
    # Derivating key points
    (x, y) = secp256k1.privtopub(privkey)
    # Returning key in corresponding format
    if not compressed:
        pk = 0x04.to_bytes(1, 'big') + x.to_bytes(sizeof(x), 'big') + y.to_bytes(sizeof(y), 'big')
    else:
        if y%2: # y is odd, so point is greater than the midpoint
            pk = 0x03.to_bytes(1, 'big') + x.to_bytes(sizeof(x), 'big')
        else: # point is less than the midpoint
            pk = 0x02.to_bytes(1, 'big') + x.to_bytes(sizeof(x), 'big')
    return pk # type : bytes


# Takes a pubkey and returns the Bitcoin address corresponding. (P2PKH)
def get_address(pubkey):
    pk_hash = int(hash160(pubkey), 16)
    # Adding the version prefix, then base58check encoding it
    version = 0x00
    address = base58check_encode(pk_hash.to_bytes(sizeof(pk_hash), 'big'), version.to_bytes(1, 'big'))
    return address # type : str