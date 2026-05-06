from dataclasses import dataclass
from typing import ClassVar
from app.backend.table_object_classes.table_object import TableObject

@dataclass
class User(TableObject):
    ROLES: ClassVar[list] = ["admin", "user", "developer", ""]
    id: int = -1
    name: str = "Anonymous"
    email: str = ""
    role: str = ""

    def __post_init__(self):
        self.check_valid_role()

    @classmethod
    def from_row(cls, row):
        """
        Takes a dictionary of attributes with associated values and creates a User object from them.
        """
        try:
            return cls(row["id"], row["name"], row["email"], row["role"])
        except (KeyError, IndexError) as e:
            raise AttributeError(f"Database Mapping Error: Column {e} not found in row passed to from_row") from e

    def to_row(self):
        return {"id": self.id, "name": self.name, "email": self.email, "role": self.role}

    def update_from_row(self, changes):
        """
        Takes a dictionary of attributes (possibly incomplete) and modifies the current User object with them.
        """
        for key, value in changes.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.check_valid_role()

    def has_higher_privilege(self, other: User) -> bool:
        """
        Returns true if the passed User has lower or equal privilege level
        """
        privilege_level_dict = {"developer": 3, "admin": 2, "user": 1}
        return privilege_level_dict[self.role] >= privilege_level_dict[other.role]

    def check_valid_role(self):
        if self.role not in self.ROLES:
            raise ValueError("Invalid role {}".format(self.role))