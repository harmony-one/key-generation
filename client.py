# we use Ethereum compatible ecdsa scheme
# SECP256k1: y^2 = x^3 + 7 over F_p, p=FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFFC2F

import json
import time
import sys
import hashlib
import getpass

from ecdsa import SigningKey, SECP256k1
from ecdsa.util import randrange_from_seed__trytryagain, string_to_number
from _pysha3 import keccak_256

import crypto
import mnemonic as mn

MIN_PASSWORD_LEN = 7
BLS12_381_ORDER=52435875175126190479447740508185965837690552500527637822603658699938581184513
SECP256k1_ORDER=115792089237316195423570985008687907852837564279074904382605163141518161494337

def is_secret_within_curve_range(secret: int,curve_order=SECP256k1_ORDER) -> bool:
    return 0 < secret < curve_order

def make_key(rnd, max_range=BLS12_381_ORDER):
  secexp = randrange_from_seed__trytryagain(rnd, max_range)
  return SigningKey.from_secret_exponent(secexp, curve=SECP256k1)

def gen_seed(num=SECP256k1.baselen):
    with open("/dev/urandom", 'rb') as f:
        seed = int.from_bytes(f.read(num), 'big')
    return seed

def gen_priv_only():
    rnd = gen_seed()
    sk = make_key(rnd)
    return sk

def get_secret_from_seed(seed):
    bip32_seed = mn.Mnemonic.mnemonic_to_seed(seed, '')
    I = crypto.hmac_oneshot(b"Harmony seed", bip32_seed, hashlib.sha512)
    master_k = I[0:32]
    secret = string_to_number(master_k)
    return secret

def get_priv_from_seed(seed):
    secret = get_secret_from_seed(seed)
    sk = SigningKey.from_secret_exponent(secret, curve=SECP256k1)
    return sk

def gen_priv_and_seed():
    secret = -1
    while not is_secret_within_curve_range(secret):
        seed = mn.Mnemonic().make_seed()
        secret = get_secret_from_seed(seed)

    sk = SigningKey.from_secret_exponent(secret, curve=SECP256k1)
    return seed, sk

def gen_priv_and_addr():
    #sk = gen_priv_only()
    seed, sk = gen_priv_and_seed()
    pk = sk.get_verifying_key().to_string()

    # get address from pubkey
    keccak = keccak_256()
    keccak.update(pk)
    addr = "0x{}".format(keccak.hexdigest()[24:])

    return seed,sk,pk,addr

def input_password():
    pw = "pw"
    pw1 = "pw1"
    while pw != pw1 or len(pw) < MIN_PASSWORD_LEN:
        pw = getpass.getpass(f"Type your password (at least {MIN_PASSWORD_LEN} chars): ")
        if len(pw) < MIN_PASSWORD_LEN:
            print(f"password has length at least {MIN_PASSWORD_LEN}")
            pw = ""
            continue
        pw1 = getpass.getpass("Type your password again: ")
        if pw != pw1:
            print("password not match!")
    return pw

def is_seed_equal(seed,seed1):
    seed = seed.strip().split()
    seed1 = seed1.strip().split()
    if len(seed) != len(seed1):
        return False
    for i in range(len(seed)):
        if seed[i] != seed1[i]:
            return False
    return True



# we don't have GUI, this is the terminal hack
def record_seed(seed):
    seed1 = ""
    print("\n\nmake terminal window wide enough to hold 12 words in one line:")
    print("write down 12 words in a paper and keep it secret\n")
    print("**********************************************************************")
    print(seed)
    print("**********************************************************************\n")
    ans = ""
    while ans != "yes" and ans != "quit":
        ans = input("write down ready? if ready type 'yes', to quit type 'quit':  ")
        sys.stdout.write("\033[F\r\033[K")
        sys.stdout.flush()

    if ans == "quit":
        return False

    sys.stdout.write("\033[3A\r\033[K\r to quit, type 'quit'\r\033[3B")
    sys.stdout.flush()
    print("enter 12 words in the same order")
    while not is_seed_equal(seed,seed1):
        seed1 = input("")
        if seed1.strip() == "quit":
            return False
        sys.stdout.write("\033[F\r\033[K")
        sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()
    return True


def decrypt_file(filename,pw):
    with open("key.json","r") as f:
        dd = json.load(f)
    sk_str = crypto.pw_decode(dd["private_key_enc"],pw,version=crypto.PW_HASH_VERSION_LATEST)
    return sk_str


def main():
    pw = input_password()

    seed, sk, pk, addr = gen_priv_and_addr()

    privkey = sk.to_string().hex()

    dd = dict()
    dd["address"] = addr
    enckey = crypto.pw_encode(privkey,pw,version=crypto.PW_HASH_VERSION_LATEST)
    dd["private_key_enc"] = enckey


    print("\nprivate key can be recovered from key.json, or from seed phrase")
    print("Keep key.json file and seed phrase secret. Don't lose them\n")
    print("**********************************************************************")
    print("Your account address: ", addr)
    print("**********************************************************************")

    if record_seed(seed):
        with open("key.json",'w') as f:
            json.dump(dd, f, indent=4)
    else:
        print("quit the key generation program, please retry again")


if __name__ == "__main__":
    main()
