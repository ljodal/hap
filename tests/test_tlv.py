from typing import Any

import pytest

from hap import tlv

CASES = [
    (
        "010568656c6c6f",
        [(tlv.IDENTIFIER, b"hello")],
    ),
    (
        # First item       Sep      Second item
        "010568656c6c6f" + "ff00" + "010568656c6c6f",
        [(tlv.IDENTIFIER, b"hello"), (tlv.IDENTIFIER, b"hello")],
    ),
    (
        "06010309ff61616161616161616161616161616161616161616161616161616161"
        "616161616161616161616161616161616161616161616161616161616161616161"
        "616161616161616161616161616161616161616161616161616161616161616161"
        "616161616161616161616161616161616161616161616161616161616161616161"
        "616161616161616161616161616161616161616161616161616161616161616161"
        "616161616161616161616161616161616161616161616161616161616161616161"
        "616161616161616161616161616161616161616161616161616161616161616161"
        "6161616161616161616161616161616161616161616161616161616161092d6161"
        "616161616161616161616161616161616161616161616161616161616161616161"
        "61616161616161616161010568656c6c6f",
        [
            (tlv.STATE, b"\x03"),
            (tlv.CERTIFICATE, b"a" * 300),
            (tlv.IDENTIFIER, b"hello"),
        ],
    ),
]


@pytest.mark.parametrize("data,expected", CASES)
def test_tlv_decode(data: str, expected: list[tuple[tlv.TLVType, Any]]) -> None:
    decoded = tlv.decode(bytes.fromhex(data))
    assert decoded == expected


@pytest.mark.parametrize(
    "expected,data",
    CASES
    + [
        (
            # First item       Sep      Second item
            "010568656c6c6f" + "ff00" + "010568656c6c6f",
            [
                (tlv.IDENTIFIER, b"hello"),
                (tlv.SEPARATOR, b""),
                (tlv.IDENTIFIER, b"hello"),
            ],
        ),
    ],
)
def test_tlv_encode(data: list[tuple[tlv.TLVType, Any]], expected: str) -> None:
    decoded = tlv.encode(data).hex()
    assert decoded == expected


@pytest.mark.parametrize("tlv_type", list(tlv.TLVType))
def test_convenience_alias(tlv_type: tlv.TLVType) -> None:
    name = tlv_type.name
    assert hasattr(tlv, name), f"TLVType.{name} is missing tlv.{name} convenience alias"
    assert getattr(tlv, name) is tlv_type, f"tlv.{name} != TLVType.{name}"
