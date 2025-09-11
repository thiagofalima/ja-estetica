from dataclasses import dataclass
from uuid import UUID
from datetime import date, datetime

@dataclass
class Client:

    _id: UUID
    name: str
    birth_date: date
    email: str
    password: str
    register_date: datetime



