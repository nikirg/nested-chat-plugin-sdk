from .schemes import SyncRequest
from typing import Callable
from fastapi import APIRouter, Request, HTTPException, status
import aiohttp
class PluginRouter(APIRouter):
    def __init__(self, api_url: str=None, plugin_name: str = None):
        super().__init__()
        self.plugin_name = plugin_name
        self.api_url = api_url
        self.create_handler = None
        self.update_handler = None
        self.delete_handler = None
        self.execute_handler = None
        self.add_api_route("/health", self._health_check, methods=["GET"])

    def on_create(self, handler: Callable):
        self.create_handler = handler
        self.add_api_route("/sync", self._handle_create, methods=["POST"])

    def on_update(self, handler: Callable):
        self.update_handler = handler
        self.add_api_route("/sync", self._handle_update, methods=["PUT"])

    def on_delete(self, handler: Callable):
        self.delete_handler = handler
        self.add_api_route("/sync", self._handle_delete, methods=["DELETE"])

    def on_execute(self, handler: Callable):
        self.execute_handler = handler
        self.add_api_route("/execute", self._handle_execute, methods=["POST"])

    async def sync(self) -> int:
        async with aiohttp.ClientSession() as session:
            payload = {"name": self.plugin_name}
            try:
                async with session.post(self.api_url, json=payload) as response:
                    return response.status
            except aiohttp.ClientError as e:
                return 404

    async def _health_check(self):
        return HTTPException(status_code=status.HTTP_200_OK, detail={"status": "available"})

    async def _handle_create(self, request_data: SyncRequest):
        if not self.create_handler:
            raise HTTPException(status_code=404, detail="Create handler not found")
        return await self.create_handler(request_data)

    async def _handle_execute(self, request: Request):
        request_data = await request.json()
        if not self.execute_handler:
            raise HTTPException(status_code=404, detail="Execute handler not found")
        return await self.execute_handler(request_data)

    async def _handle_update(self, request_data: SyncRequest):
        if not self.update_handler:
            raise HTTPException(status_code=404, detail="Update handler not found")
        return await self.update_handler(request_data)

    async def _handle_delete(self, request_data: SyncRequest):
        if not self.delete_handler:
            raise HTTPException(status_code=404, detail="Delete handler not found")
        return await self.delete_handler(request_data)
