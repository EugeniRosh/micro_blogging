from dataclasses import dataclass


@dataclass
class NotificationsAdminDTO:
    users: str
    text: str
