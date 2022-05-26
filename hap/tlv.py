"""
Encoding and decoding of type-length-value (TLV) encoded values.
"""

import struct
from enum import IntEnum


class TLVType(IntEnum):
    METHOD = 0x00
    IDENTIFIER = 0x01
    SALT = 0x02
    PUBLIC_KEY = 0x03
    PROOF = 0x04
    ENCRYPTED_DATA = 0x05
    STATE = 0x06
    ERROR = 0x07
    RETRY_DELAY = 0x08
    CERTIFICATE = 0x09
    SIGNATURE = 0x0A
    PERMISSIONS = 0x0B
    FRAGMENT_DATA = 0x0C
    FRAGMENT_LAST = 0x0D
    FLAGS = 0x13
    SEPARATOR = 0xFF

    def __call__(self, value: bytes) -> tuple["TLVType", bytes]:
        """
        Convenience helper to create a tuple with a TLV type and value.

        .. code-block:: python
            IDENTIFIER(b"hello") == (IDENTIFIER, b"hello")
        """

        return (self, value)


# Convenience aliases for TLV types
METHOD = TLVType.METHOD
IDENTIFIER = TLVType.IDENTIFIER
SALT = TLVType.SALT
PUBLIC_KEY = TLVType.PUBLIC_KEY
PROOF = TLVType.PROOF
ENCRYPTED_DATA = TLVType.ENCRYPTED_DATA
STATE = TLVType.STATE
ERROR = TLVType.ERROR
RETRY_DELAY = TLVType.RETRY_DELAY
CERTIFICATE = TLVType.CERTIFICATE
SIGNATURE = TLVType.SIGNATURE
PERMISSIONS = TLVType.PERMISSIONS
FRAGMENT_DATA = TLVType.FRAGMENT_DATA
FRAGMENT_LAST = TLVType.FRAGMENT_LAST
FLAGS = TLVType.FLAGS
SEPARATOR = TLVType.SEPARATOR


def decode(data: bytes) -> list[tuple[TLVType, bytes]]:
    """
    Split one or more TLV encoded values.

    >>> decode(bytes.fromhex("010568656c6c6f"))
    [(tlv.IDENTIFIER, b'hello')]
    """

    values = []
    while data:
        if len(data) < 2:
            raise ValueError("TLV value must be at least two bytes long")

        # The first two bytes are the data type and the length of the value
        tlv_type, length = data[0], data[1]

        if len(data) < 2 + length:
            raise ValueError(
                "Invalid TLV value. Expected {length+2} bytes, but only got {len(data)}"
            )

        if tlv_type == TLVType.SEPARATOR and length != 0:
            raise ValueError(
                f"Invalid TLV value. Separator should be zero-length, was {length}"
            )

        value = data[2 : 2 + length]
        data = data[2 + length :]

        # Skip separators
        if tlv_type == TLVType.SEPARATOR:
            continue

        # Combine fragmented messages
        while len(data) >= 2 and data[0] == tlv_type:
            length = data[1]
            if len(data) < 2 + length:
                raise ValueError(
                    "Invalid TLV value. Expected {length+2} bytes, but only got {len(data)}"
                )
            value += data[2 : 2 + length]
            data = data[2 + length :]

        try:
            values.append((TLVType(tlv_type), value))
        except ValueError:
            # Ignore unknown TLV types, as per the spec
            pass

    return values


def encode(values: list[tuple[TLVType, bytes]]) -> bytes:
    """
    Encode the provided values to bytes.

    >>> encode([(tlv.IDENTIFIER, b"hello")]).hex()
    '010568656c6c6f'
    """

    max_len = 255
    fragments = []

    for i, (tlv_type, value) in enumerate(values):
        for j in range(0, len(value), max_len):
            fragment = value[j : j + max_len]
            fragments.append(struct.pack("BB", tlv_type, len(fragment)))
            fragments.append(fragment)

        # If value is empty the loop above will not run
        if not value:
            fragments.append(struct.pack("BB", tlv_type, 0))

        # Add a separator if the next element has the same type
        if len(values) > i + 1 and values[i + 1][0] == tlv_type:
            fragments.append(struct.pack("BB", SEPARATOR, 0))

    return b"".join(fragments)
