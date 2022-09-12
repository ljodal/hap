from typing import Callable

import pytest

from hap.accessories import (
    Accessory,
    AccessoryInformation,
    FirmwareRevision,
    Identify,
    Manufacturer,
    Model,
    Name,
    SerialNumber,
    Service,
)
from hap.backends.base import TypeManager

pytest.register_assert_rewrite("tests.fixtures")

from .fixtures import Client  # noqa: E402


@pytest.fixture
def get_instance_id() -> Callable[[], int]:
    class IIDGenerator:
        prev_iid = 0

        def __call__(self) -> int:
            iid = self.prev_iid = self.prev_iid + 1
            return iid

    return IIDGenerator()


@pytest.fixture
def service(get_instance_id: Callable[[], int]) -> Service:
    return Service.from_spec(
        AccessoryInformation(
            FirmwareRevision("0.0.1"),  # type: ignore[arg-type]
            Identify(),
            Manufacturer("Drugis Corp."),  # type: ignore[arg-type]
            Model("Test model"),  # type: ignore[arg-type]
            Name("Test name"),  # type: ignore[arg-type]
            SerialNumber("123"),  # type: ignore[arg-type]
        ),
        get_instance_id,
    )


@pytest.fixture
def accessory(service: Service) -> Accessory:
    return Accessory(aid=1, services=[service])


@pytest.fixture
def type_manager() -> TypeManager:
    return TypeManager()


@pytest.fixture
def client() -> Client:
    """
    Get a simple HTTP client that can communicate with an accessory server.
    """

    return Client()
