from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


def verify(public_key: bytes, signature: bytes, msg: bytes) -> None:
    try:
        Ed25519PublicKey.from_public_bytes(public_key).verify(signature, msg)
    except InvalidSignature as e:
        raise ValueError("Invalid ed25519 signature") from e


def generate_private_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.generate()


def get_public_key(private_key: Ed25519PrivateKey) -> bytes:
    return private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
