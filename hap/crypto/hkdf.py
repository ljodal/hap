import hmac
from math import ceil

hash_len = 32


def hmac_sha256(key: bytes, data: bytes) -> bytes:
    return hmac.digest(key, data, "sha512")


def hkdf(key: bytes, salt: bytes, info: bytes, length: int = 32) -> bytes:
    """Key derivation function"""
    if len(salt) == 0:
        salt = bytes([0] * hash_len)
    prk = hmac_sha256(salt, key)
    t = b""
    okm = b""
    for i in range(ceil(length / hash_len)):
        t = hmac_sha256(prk, t + info + bytes([i + 1]))
        okm += t
    return okm[:length]
