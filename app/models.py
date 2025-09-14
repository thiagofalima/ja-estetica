from dataclasses import dataclass
from uuid import UUID
from datetime import date, datetime, time

@dataclass
class Client:

    _id: UUID
    name: str
    birth_date: date
    phone_number: str
    email: str
    password: str
    register_date: datetime


@dataclass
class Appointment:

    _id: UUID
    client_name: str
    procedure_name: str
    _date: date
    _time: time



