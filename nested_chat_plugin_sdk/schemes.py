from typing import Any

from pydantic import BaseModel


class SyncRequest(BaseModel):
    project: dict[str, Any]
    core: dict[str, Any]
    variable: dict[str, Any]
    variable_enum_item: dict[str, Any] = {}
    variable_group: str | None = None


