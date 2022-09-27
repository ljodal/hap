from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Generic, Iterable, TypeVar
from uuid import UUID

from typing_extensions import NamedTuple

T = TypeVar("T")
Number = int | float


# Service and characteristic type definitions
#
# Classes that represent types of services and characteristics. These are used
# to define both Apple's pre-defined ones and can also be used to define custom
# ones.


class Permission(str, Enum):
    PAIRED_READ = "pr"
    PAIRED_WRITE = "pw"
    NOTIFY = "ev"
    ADDITIONAL_AUTHORIZATION = "aa"
    TIMED_WRITE = "tw"
    HIDDEN = "hd"
    WRITE_RESPONSE = "wr"


class CharacteristicType(NamedTuple, Generic[T]):
    """
    A specification of a characteristic, whithout any actual data.
    """

    uuid: UUID
    permissions: tuple[Permission, ...]
    format: str
    ev: bool | None = None
    description: str | None = None
    unit: str | None = None
    min_value: Number | None = None
    max_value: Number | None = None
    min_step: Number | None = None
    max_length: int | None = None
    max_data_length: int | None = None
    valid_values: tuple[T, ...] | None = None
    valid_values_range: tuple[T, T] | None = None

    def __str__(self) -> str:
        if self.description:
            return f"{self.uuid} ({self.description})"
        return f'"{self.uuid}"'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self)})"

    def __call__(
        self,
        initial_value: T | None = None,
        event_notifications_enabled: bool = False,
    ) -> CharacteristicSpec[T]:
        """
        Define a characteristic spec. The returned spec is immutable and can be reused.
        """

        return CharacteristicSpec(self, initial_value, event_notifications_enabled)


class ServiceType(NamedTuple):
    """
    A service type is a definition of a service that an accessory can expose.
    It has an unique ID, a name and set of required and optional
    characteristics. You can define your own servce types, but typically you
    will use Apple's pre-defined ones.
    """

    uuid: UUID
    name: str
    required_characteristics: tuple[CharacteristicType[Any], ...]
    optional_characteristics: tuple[CharacteristicType[Any], ...]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self)})"

    def __call__(
        self,
        *characteristics: CharacteristicSpec[Any],
        primary: bool = False,
        hidden: bool = False,
    ) -> ServiceSpec:
        """
        Define a service spec. The returned spec is immutable and can be reused.
        """

        characteristics = tuple(characteristics)
        char_types = {char.type for char in characteristics}

        if unsupported_char_types := {
            char_type
            for char_type in char_types
            if char_type not in self.required_characteristics
            and char_type not in self.optional_characteristics
        }:
            names = ", ".join(
                char_type.description or str(char_type.uuid)
                for char_type in unsupported_char_types
            )
            raise ValueError(f'Unsupported characteristics for "{self.name}": {names}')

        if missing_char_types := {
            char_type
            for char_type in self.required_characteristics
            if char_type not in char_types
        }:
            names = ", ".join(
                char_type.description or str(char_type.uuid)
                for char_type in missing_char_types
            )
            raise ValueError(
                f'Missing requred characteristics for "{self.name}": {names}'
            )

        return ServiceSpec(self, characteristics, primary, hidden)


# Specs
#
# Spec types represent a service or characteristics that's unbound, meaning
# that they don't contain any state, are immutable and can be reused. These are
# not intended to be used directly, but rather through the characteristics
# types.


class CharacteristicSpec(NamedTuple, Generic[T]):
    type: CharacteristicType[T]
    initial_value: T | None
    event_notifications_enabled: bool


class ServiceSpec(NamedTuple):
    type: ServiceType
    characteristics: tuple[CharacteristicSpec[Any], ...]
    primary: bool
    hidden: bool


# Bound instance
#
# The final classes in this module represent bound instances of characteristics
# and service, that is stateful instances connected to a specific accessory.


class Characteristic(Generic[T]):
    """
    An instance of a characteristics, bound to a service.

    You typically don't use this directly, but rather instantiate it from one
    of Apple's pre-defined characteristics.
    """

    def __init__(
        self,
        iid: int,
        type: CharacteristicType[T],
        event_notifications_enabled: bool,
        initial_value: T | None,
    ) -> None:
        self.iid = iid
        self.type = type
        self.event_notifications_enabled = event_notifications_enabled
        self._value: T | None = initial_value
        self._ttl: int | None = None
        self._pid: int | None = None

    @classmethod
    def from_spec(
        cls,
        spec: CharacteristicSpec[Any],
        get_instance_id: Callable[[], int],
    ) -> Characteristic[Any]:
        return Characteristic(
            iid=get_instance_id(),
            type=spec.type,
            event_notifications_enabled=spec.event_notifications_enabled,
            initial_value=spec.initial_value,
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__qualname__} "
            f"iid={self.iid} type={self.type.uuid} "
            f"event_notifications_enabled={self.event_notifications_enabled} "
            f"value={self._value} ttl={self._ttl} pid={self._pid}>"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Characteristic):
            return NotImplemented
        return (
            other.iid == self.iid
            and other.type == self.type
            and other.event_notifications_enabled == self.event_notifications_enabled
            and other._value == self._value
            and other._ttl == self._ttl
            and other._pid == self._pid
        )

    @property
    def value(self) -> T | None:
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        self._value = value


class Service:
    """
    An instance of a service, bound to an accessory.
    """

    # TODO: Support linked services

    def __init__(
        self,
        iid: int,
        type: ServiceType,
        characteristics: Iterable[Characteristic[Any]],
        primary: bool,
        hidden: bool,
    ) -> None:
        self.iid = iid
        self.type = type
        self.characteristics: tuple[Characteristic[Any], ...] = tuple(characteristics)
        self.hidden = hidden
        self.primary = primary

    @classmethod
    def from_spec(
        cls, spec: ServiceSpec, get_instance_id: Callable[[], int]
    ) -> Service:
        return Service(
            iid=get_instance_id(),
            type=spec.type,
            primary=spec.primary,
            hidden=spec.hidden,
            characteristics=(
                Characteristic.from_spec(characteristic_spec, get_instance_id)
                for characteristic_spec in spec.characteristics
            ),
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__qualname__} "
            f"iid={self.iid} type={self.type.uuid} "
            f"characteristics={self.characteristics} "
            f"hidden={self.hidden} primary={self.primary}>"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Service):
            return NotImplemented
        return (
            other.iid == self.iid
            and other.type == self.type
            and other.characteristics == self.characteristics
            and other.hidden == self.hidden
            and other.primary == self.primary
        )

    def __getitem__(self, key: CharacteristicType[T]) -> Characteristic[T]:
        if char := next(
            (char for char in self.characteristics if char.type == key), None
        ):
            return char
        raise KeyError(f'Service as no "{key}" characteristic')

    def __setitem__(self, key: CharacteristicType[T], value: T) -> None:
        characteristic: Characteristic[T] = self[key]
        characteristic.value = value


class Accessory:
    """
    An accessory is a collection of services, identified by a ID that's unique
    to the accessory server.
    """

    def __init__(self, aid: int, services: Iterable[Service]) -> None:
        self.aid = aid
        self.services: tuple[Service, ...] = tuple(services)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__qualname__} aid={self.aid} services={self.services}>"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Accessory):
            return NotImplemented
        return other.aid == self.aid and other.services == self.services

    def __getitem__(self, key: ServiceType) -> Service:
        if service := next(
            (service for service in self.services if service.type == key), None
        ):
            return service
        raise KeyError(f'Accessory as no "{key}" service')
