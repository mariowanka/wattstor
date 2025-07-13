from uuid import UUID

from attrs import define


@define
class User:
    id: UUID
    username: str
    is_technician: bool
