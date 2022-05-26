from typing import Any, TypedDict

from ..accessories import Accessory, Characteristic, Service
from .base import TypeManager


class CharacteristicState(TypedDict):
    iid: int
    uuid: str
    event_notifications_enabled: bool
    value: Any


class ServiceState(TypedDict):
    iid: int
    uuid: str
    primary: bool
    hidden: bool
    characteristics: list[CharacteristicState]


class State(TypedDict):
    accessories: dict[int, list[ServiceState]]


class MemoryBackend:
    def __init__(self) -> None:
        self.state: State = {"accessories": {}}

    async def load_accessories(self, types: TypeManager) -> list[Accessory]:
        def hydrate_characteristic(
            characteristic: CharacteristicState,
        ) -> Characteristic[Any]:
            characteristic_type = types.get_characteristic(characteristic["uuid"])

            return Characteristic(
                iid=characteristic["iid"],
                type=characteristic_type,
                initial_value=characteristic["value"],
                event_notifications_enabled=characteristic[
                    "event_notifications_enabled"
                ],
            )

        def hydrate_service(service: ServiceState) -> Service:
            characteristics = [
                hydrate_characteristic(characteristic)
                for characteristic in service["characteristics"]
            ]

            service_type = types.get_service(service["uuid"])

            return Service(
                iid=service["iid"],
                type=service_type,
                primary=service["primary"],
                hidden=service["hidden"],
                characteristics=characteristics,
            )

        return [
            Accessory(
                aid=aid, services=[hydrate_service(service) for service in services]
            )
            for aid, services in self.state["accessories"].items()
        ]

    async def store_accessory(self, accessory: Accessory) -> None:
        self.state["accessories"][accessory.aid] = [
            ServiceState(
                iid=service.iid,
                uuid=str(service.type.uuid),
                primary=service.primary,
                hidden=service.hidden,
                characteristics=[
                    CharacteristicState(
                        iid=characteristic.iid,
                        uuid=str(characteristic.type.uuid),
                        event_notifications_enabled=characteristic.event_notifications_enabled,
                        value=characteristic.value,
                    )
                    for characteristic in service.characteristics
                ],
            )
            for service in accessory.services
        ]
