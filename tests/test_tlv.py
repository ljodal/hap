from typing import Any

import pytest

from hap import tlv

CASES = (
    (
        "010568656c6c6f",
        [tlv.Identifier("hello")],
    ),
    (
        # First item       Sep      Second item
        "010568656c6c6f" + "ff00" + "010568656c6c6f",
        [tlv.Identifier("hello"), tlv.Identifier("hello")],
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
            tlv.State(3),
            tlv.Certificate(b"a" * 300),
            tlv.Identifier("hello"),
        ],
    ),
)

CASE_IDS = ("single value", "values with separator", "split value")


@pytest.mark.parametrize("data,expected", CASES, ids=CASE_IDS)
def test_tlv_decode(data: str, expected: list[tlv.TLV[Any]]) -> None:
    decoded = tlv.decode(bytes.fromhex(data))
    assert decoded == expected


@pytest.mark.parametrize(
    "expected,values",
    CASES
    + (
        (
            # First item       Sep      Second item
            "010568656c6c6f" + "ff00" + "010568656c6c6f",
            [tlv.Identifier("hello"), tlv.Separator(), tlv.Identifier("hello")],
        ),
    ),
    ids=CASE_IDS + ("values with explicit separator",),
)
def test_tlv_encode(values: list[tlv.TLV[Any]], expected: str) -> None:
    decoded = tlv.encode(*values).hex()
    assert decoded == expected


@pytest.mark.parametrize("tlv_type", list(tlv.TLVType))
def test_convenience_alias(tlv_type: tlv.TLVType) -> None:
    name = tlv_type.name
    cls_name = name.replace("_", " ").title().replace(" ", "")
    assert hasattr(tlv, cls_name), f"TLVType.{name} is missing tlv.{cls_name} class"
    cls = getattr(tlv, cls_name)
    assert issubclass(cls, tlv.TLV)
    assert hasattr(cls, "tlv_type")
    assert cls.tlv_type is tlv_type, f"tlv.{cls_name}.tlv_type != TLVType.{name}"
