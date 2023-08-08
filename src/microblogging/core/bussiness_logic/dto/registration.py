from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegistrationDTO:
    username: str
    email: str
    password: str
    date_of_birth: datetime
    role = "user"
