from enum import Enum


class RoleEnum(str, Enum):
    Admin = "Admin"
    User = "User"
    Editor = "Editor"