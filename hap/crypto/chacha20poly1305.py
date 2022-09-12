from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def encrypt(key: bytes, nonce: bytes, msg: bytes) -> bytes:
    """
    Encrypt the given message according to Apple's instructions.
    """

    return ChaCha20Poly1305(key).encrypt(nonce, msg, associated_data=None)


def decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypt the given message according to Apple's instructions.
    """

    try:
        return ChaCha20Poly1305(key).decrypt(nonce, ciphertext, associated_data=None)
    except InvalidTag as e:
        raise ValueError("Unable to decrypt value") from e
