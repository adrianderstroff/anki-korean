import hashlib


def sdbm_hash_string(str):
    h = 0
    m = (1 << 32)
    for i in str:
        t = h
        h = (t << 6) % m + (t << 16) % m - t + ord(i)
        h %= m
    return h


def create_id(name):
    result = hashlib.md5(str.encode(name))
    numbers = result.hexdigest()
    numbers = sdbm_hash_string(numbers)
    return numbers
