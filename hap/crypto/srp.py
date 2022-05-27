#
# Copyright 2019 aiohomekit team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Implements the Secure Remote Password (SRP) algorithm. More information can be
found on https://tools.ietf.org/html/rfc5054. See HomeKit spec page 36 for
adjustments imposed by Apple.

Adapted from aiohomekit's implementation.
"""
import hashlib
import math
import os


def to_bytes(num: int) -> bytes:
    return num.to_bytes(int(math.ceil(num.bit_length() / 8)), "big")


def generate_private_key() -> int:
    """
    Static function to generate a 16 byte random key.

    :return: the key as an integer
    """
    return int.from_bytes(os.urandom(16), byteorder="big")


def generate_salt() -> bytes:
    return os.urandom(16)


class SRP:
    def __init__(self, username: str, password: str, salt: bytes) -> None:
        # generator as defined by 3072bit group of RFC 5054
        self.g = int(b"5", 16)
        # modulus as defined by 3072bit group of RFC 5054
        self.n = int(
            b"FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E08"
            b"8A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B"
            b"302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9"
            b"A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE6"
            b"49286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8"
            b"FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D"
            b"670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C"
            b"180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF695581718"
            b"3995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D"
            b"04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7D"
            b"B3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D226"
            b"1AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200C"
            b"BBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFC"
            b"E0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF",
            16,
        )
        # HomeKit requires SHA-512 (See page 36)
        self.h = hashlib.sha512

        self.A: bytes | None = None
        self.B: bytes | None = None

        self.username = username
        self.password = password
        self.salt = salt

    @property
    def k(self) -> int:
        # calculate k (see https://tools.ietf.org/html/rfc5054#section-2.5.3)
        hash_instance = self.h()
        n = to_bytes(self.n)
        g = bytes.fromhex(383 * "00" + "05")  # 383 * b'0' + '5'.encode()
        hash_instance.update(n)
        hash_instance.update(g)
        k = int.from_bytes(hash_instance.digest(), "big")
        return k

    @property
    def u(self) -> int:
        if self.A is None:
            raise RuntimeError("Client's public key is missing")
        if self.B is None:
            raise RuntimeError("Server's public key is missing")
        hash_instance = self.h()
        hash_instance.update(self.A)
        hash_instance.update(self.B)
        u = int.from_bytes(hash_instance.digest(), "big")
        return u

    def get_session_key(self) -> bytes:
        hash_instance = self.h()
        hash_instance.update(self.get_shared_secret())
        return hash_instance.digest()

    @property
    def x(self) -> int:
        i = (self.username + ":" + self.password).encode()
        hash_instance = self.h()
        hash_instance.update(i)
        hash_value = hash_instance.digest()

        hash_instance = self.h()
        hash_instance.update(self.salt)
        hash_instance.update(hash_value)

        return int.from_bytes(hash_instance.digest(), "big")

    def get_shared_secret(self) -> bytes:
        raise NotImplementedError()


class Client(SRP):
    """
    Implements all functions that are required to simulate an iOS HomeKit controller
    """

    def __init__(self, username: str, password: str, salt: bytes, B: bytes) -> None:
        super().__init__(username, password, salt)
        self.a = generate_private_key()
        self.A: bytes = to_bytes(pow(self.g, self.a, self.n))
        self.B: bytes = B

    @property
    def public_key(self) -> bytes:
        return to_bytes(pow(self.g, self.a, self.n))

    def get_shared_secret(self) -> bytes:
        u = self.u
        x = self.x
        tmp1 = int.from_bytes(self.B, "big") - (self.k * pow(self.g, x, self.n))
        tmp2 = self.a + (u * x)  # % self.n
        return to_bytes(pow(tmp1, tmp2, self.n))

    def get_proof(self) -> bytes:
        hash_instance = self.h()
        hash_instance.update(to_bytes(self.n))
        hN = bytearray(hash_instance.digest())

        hash_instance = self.h()
        hash_instance.update(to_bytes(self.g))
        hg = bytes(hash_instance.digest())

        for index in range(0, len(hN)):
            hN[index] ^= hg[index]

        u = self.username.encode()
        hash_instance = self.h()
        hash_instance.update(u)
        hu = hash_instance.digest()
        K = self.get_session_key()

        hash_instance = self.h()
        hash_instance.update(hN)
        hash_instance.update(hu)
        hash_instance.update(self.salt)
        hash_instance.update(self.A)
        hash_instance.update(self.B)
        hash_instance.update(K)
        return hash_instance.digest()

    def verify_servers_proof(self, M: int | bytes) -> bool:
        if isinstance(M, bytes):
            tmp = int.from_bytes(M, "big")
        else:
            tmp = M
        hash_instance = self.h()
        hash_instance.update(self.A)
        hash_instance.update(self.get_proof())
        hash_instance.update(self.get_session_key())
        return tmp == int.from_bytes(hash_instance.digest(), "big")


class Server(SRP):
    """
    Implements all functions that are required to simulate an iOS HomeKit accessory
    """

    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password, salt=generate_salt())
        self.b = generate_private_key()
        g_b = pow(self.g, self.b, self.n)
        self.B: bytes = to_bytes((self.k * self.verifier + g_b) % self.n)

    @property
    def verifier(self) -> int:
        hash_value = self.x
        v = pow(self.g, hash_value, self.n)
        return v

    def set_client_public_key(self, A: bytes) -> None:
        self.A = A

    @property
    def public_key(self) -> bytes:
        return self.B

    def get_shared_secret(self) -> bytes:
        if self.A is None:
            raise TypeError("Client's public key is missing")

        tmp1 = int.from_bytes(self.A, "big") * pow(self.verifier, self.u, self.n)
        return to_bytes(pow(tmp1, self.b, self.n))

    def verify_clients_proof(self, m: bytes) -> bool:
        if self.A is None:
            raise TypeError("Client's public key is missing")

        hash_instance = self.h()
        hash_instance.update(to_bytes(self.n))
        hN = bytearray(hash_instance.digest())

        hash_instance = self.h()
        hash_instance.update(to_bytes(self.g))
        hg = hash_instance.digest()

        for index in range(0, len(hN)):
            hN[index] ^= hg[index]

        u = self.username.encode()
        hash_instance = self.h()
        hash_instance.update(u)
        hu = hash_instance.digest()
        K = self.get_session_key()

        hash_instance = self.h()
        hash_instance.update(hN)
        hash_instance.update(hu)
        hash_instance.update(self.salt)
        hash_instance.update(self.A)
        hash_instance.update(self.B)
        hash_instance.update(K)
        return m == hash_instance.digest()

    def get_proof(self, m: bytes) -> bytes:
        if self.A is None:
            raise TypeError("Client's public key is missing")

        hash_instance = self.h()
        hash_instance.update(self.A)
        hash_instance.update(m)
        hash_instance.update(self.get_session_key())
        return hash_instance.digest()
