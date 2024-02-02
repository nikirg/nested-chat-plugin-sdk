

# Plugin SDK for FastAPI

The Plugin SDK nested-chat-plugin-sdk is a FastAPI extension that provides a convenient way to handle requests for creating, updating, deleting, and executing operations.

## Installation

Install dependencies using Poetry and activate the virtual environment. [Learn how to install Poetry](https://python-poetry.org/docs/)

```bash
poetry install
poetry shell
````

Install the SDK using [Poetry](https://python-poetry.org/):

```bash
poetry add nested-chat-plugin-sdk
```

## Example
```python
from fastapi import FastAPI, Request
from nested_chat_plugin_sdk.sdk import PluginRouter, SyncRequest

app = FastAPI()
plugin_router = PluginRouter(api_url="")

@plugin_router.on_create
async def handle_create(data: SyncRequest):
    print("create", data)

@plugin_router.on_update
async def handle_update(data: SyncRequest):
    print("update", data)

@plugin_router.on_delete
async def handle_delete(data: SyncRequest):
    print("delete", data)

@plugin_router.on_execute
async def handle_execute(request: Request):
    print("execute", request)

app.include_router(plugin_router)

```

## API Routes

### `/sync`

- `POST`: Create data
- `PUT`: Update data
- `DELETE`: Delete data

### `/execute`

- `POST`: Execute operation

## SyncRequest Schema

```python
from nested_chat_plugin_sdk.schemes import SyncRequest

class SyncRequest(BaseModel):
    project: dict[str, Any]
    core: dict[str, Any]
    variable: dict[str, Any]
    variable_enum_item: dict[str, Any] = {}
    variable_group: str | None = None


```



