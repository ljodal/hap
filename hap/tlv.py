"""
Encoding and decoding of type-length-value (TLV) encoded values.
"""

import math
import struct
from enum import IntEnum
from typing import Any, Callable, ClassVar, Generic, Sequence, TypeVar


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


T = TypeVar("T")
S = TypeVar("S")


class TLV(Generic[T]):
    __match_args__ = ("_value",)

    tlv_type: ClassVar[TLVType]

    def __init__(self, value: T) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"tlv.{type(self).__name__}({self._value!r})"

    def __repr__(self) -> str:
        return str(self)

    def encode(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def decode(cls: type[S], data: bytes) -> S:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TLV):
            return NotImplemented

        return self.tlv_type == other.tlv_type and self._value == other._value


_REGISTRY: dict[TLVType, type[TLV[Any]]] = {}


def tlv(
    name: str,
    tlv_type: TLVType,
    /,
    encoder: Callable[[T], bytes],
    decoder: Callable[[bytes], T],
) -> type[TLV[T]]:
    """
    Helper to create a TLV sublass. This creates the encoding and decoding
    methods and also registers the type in the registry. If a class with the
    same type already exists an error is raised.
    """

    if tlv_type in _REGISTRY:
        raise ValueError(
            f"A class has already been created for TLV type {tlv_type.name}"
        )

    def encode(self: TLV[T]) -> bytes:
        return encoder(self._value)

    def decode(cls: type[TLV[T]], data: bytes) -> TLV[T]:
        return cls(decoder(data))

    _REGISTRY[tlv_type] = cls = type(
        name,
        (TLV,),
        {"tlv_type": tlv_type, "encode": encode, "decode": classmethod(decode)},
    )
    return cls


def tlv_bytes(name: str, tlv_type: TLVType) -> type[TLV[bytes]]:
    return tlv(name, tlv_type, encoder=lambda data: data, decoder=lambda value: value)


def tlv_int(name: str, tlv_type: TLVType) -> type[TLV[int]]:
    return tlv(
        name,
        tlv_type,
        encoder=lambda value: value.to_bytes(
            int(math.ceil(value.bit_length() / 8)), "little"
        ),
        decoder=lambda data: int.from_bytes(data, "little"),
    )


def tlv_str(name: str, tlv_type: TLVType) -> type[TLV[str]]:
    return tlv(
        name,
        tlv_type,
        encoder=lambda value: value.encode("utf-8"),
        decoder=lambda data: data.decode("utf-8"),
    )


Method = tlv_int("Method", TLVType.METHOD)
Identifier = tlv_str("Identifier", TLVType.IDENTIFIER)
Salt = tlv_bytes("Salt", TLVType.SALT)
PublicKey = tlv_bytes("PulicKey", TLVType.PUBLIC_KEY)
Proof = tlv_bytes("Proof", TLVType.PROOF)
EncryptedData = tlv_bytes("EncryptedData", TLVType.ENCRYPTED_DATA)
State = tlv_int("State", TLVType.STATE)
Error = tlv_int("Error", TLVType.ERROR)
RetryDelay = tlv_int("RetryDelay", TLVType.RETRY_DELAY)
Certificate = tlv_bytes("Certificate", TLVType.CERTIFICATE)
Signature = tlv_bytes("Signature", TLVType.SIGNATURE)
Permissions = tlv_int("Permissions", TLVType.PERMISSIONS)
FragmentData = tlv_bytes("FragmentData", TLVType.FRAGMENT_DATA)
FragmentLast = tlv_bytes("FragmentLast", TLVType.FRAGMENT_LAST)
Flags = tlv_int("Flags", TLVType.FLAGS)


class Separator(TLV[None]):
    tlv_type = TLVType.SEPARATOR

    def __init__(self) -> None:
        super().__init__(None)

    def encode(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "Separator":
        if data != b"":
            raise ValueError(b"Unexpected data for TLV separator: {data}")
        return cls()


_REGISTRY[TLVType.SEPARATOR] = Separator


def decode(data: bytes) -> list[TLV[Any]]:
    """
    Split one or more TLV encoded values.

    >>> decode(bytes.fromhex("010568656c6c6f"))
    [(tlv.IDENTIFIER, b'hello')]
    """

    values: list[TLV[Any]] = []
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
            tlv_cls = _REGISTRY[TLVType(tlv_type)]
            values.append(tlv_cls.decode(value))
        except (ValueError, IndexError):
            # Ignore unknown TLV types, as per the spec
            pass

    return values


def encode(values: Sequence[TLV[Any]]) -> bytes:
    """
    Encode the provided values to bytes.

    >>> encode([(tlv.IDENTIFIER, b"hello")]).hex()
    '010568656c6c6f'
    """

    max_len = 255
    fragments = []

    for i, tlv in enumerate(values):
        value = tlv.encode()
        for j in range(0, len(value), max_len):
            fragment = value[j : j + max_len]
            fragments.append(struct.pack("BB", tlv.tlv_type, len(fragment)))
            fragments.append(fragment)

        # If value is empty the loop above will not run
        if not value:
            fragments.append(struct.pack("BB", tlv.tlv_type, 0))

        # Add a separator if the next element has the same type
        if len(values) > i + 1 and values[i + 1].tlv_type == tlv.tlv_type:
            fragments.append(struct.pack("BB", TLVType.SEPARATOR, 0))

    return b"".join(fragments)
