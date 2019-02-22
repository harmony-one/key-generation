# we use Ethereum compatible ecdsa scheme
# SECP256k1: y2 = x3 + 7 over F_p, p=FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFFC2F

import json
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import randrange_from_seed__trytryagain
from _pysha3 import keccak_256

def make_key(seed):
  secexp = randrange_from_seed__trytryagain(seed, SECP256k1.order)
  return SigningKey.from_secret_exponent(secexp, curve=SECP256k1)

def gen_seed(num=SECP256k1.baselen):
    with open("/dev/urandom", 'rb') as f:
        seed = int.from_bytes(f.read(num), 'big')
    return seed

def gen_priv_pub_keys():
    seed = gen_seed()
    sk = make_key(seed)
    pk = sk.get_verifying_key().to_string()

    # get address from pubkey
    keccak = keccak_256()
    keccak.update(pk)
    addr = "0x{}".format(keccak.hexdigest()[24:])

    return seed, sk,pk,addr


def main():
    seed, sk, pk, addr = gen_priv_pub_keys()
    print("\n**********************************")
    print("Keep your private key file secret!!")
    print("Don't lose your private key!!")
    print("We cannot recover your account if you lose your private key!!")
    print("**********************************\n")

    # print("seed is ", seed)
    print("private key: ", sk.to_string().hex())
    print("account address: ", addr)
    print("private key file saved to key.json")
    print("**********************************\n")

    dd = dict()
    dd["private_key"] = sk.to_string().hex()
    dd["address"] = addr
    with open("key.json",'w') as f:
        json.dump(dd, f, indent=4)


if __name__ == "__main__":
    main()
