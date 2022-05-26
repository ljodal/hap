import asyncio
from pathlib import Path

from hap.accessories import Accessory
from hap.backends.base import TypeManager
from hap.backends.file import FileBackend


def test_file_backend(
    accessory: Accessory, type_manager: TypeManager, tmp_path: Path
) -> None:
    path = tmp_path / "state.json"

    backend = FileBackend(path=path)

    assert asyncio.run(backend.load_accessories(type_manager)) == []
    asyncio.run(backend.store_accessory(accessory))
    assert asyncio.run(backend.load_accessories(type_manager)) == [accessory]
