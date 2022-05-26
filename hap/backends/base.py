from typing import Any, Protocol
from uuid import UUID

from ..accessories import (
    Accessory,
    CharacteristicType,
    ServiceType,
    characteristics,
    services,
)


class TypeManager:
    def __init__(self) -> None:
        self.characteristics = {
            char.uuid: char
            for char in (
                getattr(characteristics, name) for name in dir(characteristics)
            )
            if isinstance(char, CharacteristicType)
        }

        self.services = {
            service.uuid: service
            for service in (getattr(services, name) for name in dir(services))
            if isinstance(service, ServiceType)
        }

    def get_characteristic(self, uuid: str | UUID) -> CharacteristicType[Any]:  # type: ignore[misc]
        if isinstance(uuid, str):
            uuid = UUID(uuid)
        return self.characteristics[uuid]

    def get_service(self, uuid: str | UUID) -> ServiceType:
        if isinstance(uuid, str):
            uuid = UUID(uuid)
        return self.services[uuid]


class Backend(Protocol):
    """
    Protocol for backend implementations for storing accessory state.
    """

    async def load_accessories(self, types: TypeManager) -> list[Accessory]:
        """
        Load all known accessories. This is called once by the accessory server
        during startup.
        """
        ...

    async def store_accessory(self, accessory: Accessory) -> None:
        """
        Store a new accesssory that was added to the accessory server.

        This should store all services and characteristic values in such a way
        that they can be fully restored through load_accessories().
        """
        ...
