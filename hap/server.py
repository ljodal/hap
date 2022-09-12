from typing import Any

from .accessories import Accessory, Characteristic, Service
from .backends import Backend


class AccessoryServer:
    """
    HAP accessory server that exposes a collection of accessories
    """

    def __init__(self, backend: Backend) -> None:
        self.accessories: list[Accessory] = []
        self.backend = backend

    def add_accessory(self, accessory: Accessory) -> None:
        """ """

        self.accessories.append(accessory)

    def on_characteristic_updated(
        self,
        accessory: Accessory,
        service: Service,
        characteristic: Characteristic[Any],
    ) -> None:
        """
        Callback when a characteristic has been updated.
        """
