import asyncio
import json
from pathlib import Path
from typing import cast

from ..accessories import Accessory
from .base import TypeManager
from .memory import MemoryBackend, State


class FileBackend(MemoryBackend):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self.lock = asyncio.Lock()
        self.has_loaded_state = False

    async def load_accessories(self, types: TypeManager) -> list[Accessory]:
        if not self.has_loaded_state:
            await self.load_state()
        return await super().load_accessories(types)

    async def store_accessory(self, accessory: Accessory) -> None:
        if not self.has_loaded_state:
            await self.load_state()
        await super().store_accessory(accessory)

    # Internal helpers

    async def load_state(self) -> None:
        loop = asyncio.get_running_loop()
        async with self.lock:
            if self.has_loaded_state:
                return
            self._state = await loop.run_in_executor(None, self._load_state)

    async def save_state(self) -> None:
        loop = asyncio.get_running_loop()
        async with self.lock:
            await loop.run_in_executor(None, self._save_state)

    def _load_state(self) -> State:
        if self.path.exists():
            with open(self.path, "r") as f:
                return cast(State, json.loads(f.read()))
        else:
            return {"accessories": {}}

    def _save_state(self) -> None:
        with open(self.path, "w") as f:
            f.write(json.dumps(self.state))
