import asyncio

from hap.accessories import Accessory
from hap.backends.base import TypeManager
from hap.backends.memory import MemoryBackend


def test_file_backend(accessory: Accessory, type_manager: TypeManager) -> None:

    backend = MemoryBackend()

    assert asyncio.run(backend.load_accessories(type_manager)) == []
    asyncio.run(backend.store_accessory(accessory))
    assert asyncio.run(backend.load_accessories(type_manager)) == [accessory]
