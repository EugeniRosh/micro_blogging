from dataclasses import dataclass


@dataclass
class AuthenticationDTO:
    email: str
    password: str
