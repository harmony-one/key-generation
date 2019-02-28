# we use Ethereum compatible ecdsa scheme
# SECP256k1: y2 = x3 + 7 over F_p, p=FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFFC2F

import json
import argparse
import getpass
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import randrange_from_seed__trytryagain
from _pysha3 import keccak_256
import crypto

MIN_PASSWORD_LEN = 7

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

def get_input_password():
    pw = "p2"
    pw1 = "pw1"
    while pw != pw1 or len(pw) < MIN_PASSWORD_LEN:
        pw = getpass.getpass("Type your password: ")
        if len(pw) < MIN_PASSWORD_LEN:
            print(f"password has length at least {MIN_PASSWORD_LEN}")
            pw = ""
            continue
        pw1 = getpass.getpass("Type your password again: ")
        if pw != pw1:
            print("password not match!")
    return pw

def main():
    parser = argparse.ArgumentParser(description='Harmony Key Generation')
    parser.add_argument('--password','-p', dest='password', action='store_true',
                        help=f"""encrypt private key using password (default: false, using random seeds instead)""")
    args = parser.parse_args()
    if args.password:
        pw = get_input_password()

    seed, sk, pk, addr = gen_priv_pub_keys()
    print("\n*******************************************")
    print("Keep key.json file secret. Don't lose it!!")
    print("********************************************")

    privkey = sk.to_string().hex()
    print("account address: ", addr)
    print("private key file saved to key.json\n")

    dd = dict()
    dd["address"] = addr
    if args.password:
        enckey = crypto.pw_encode(privkey,pw,version=crypto.PW_HASH_VERSION_LATEST)
        deckey = crypto.pw_decode(enckey,pw,version=crypto.PW_HASH_VERSION_LATEST)
        dd["private_key_enc"] = enckey
    else:
        dd["private_key"] = privkey

    with open("key.json",'w') as f:
        json.dump(dd, f, indent=4)


if __name__ == "__main__":
    main()
