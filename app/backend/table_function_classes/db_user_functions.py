from app.backend.db import DB
from app.backend.table_object_classes.user import User
import warnings

class DBUserFunctions:
    def __init__(self, db:DB):
        self.DB = db

    def add_user(self, user: User):
        """
        Takes a User object and creates an insertion command using values from the attributes of the object.
        """
        if user.id == -1:
            command = "INSERT INTO Users (name, email, role) VALUES (?, ?, ?)"
            params = (user.name, user.email, user.role)
        else: # Attempt to add this user which has a non-default ID.
            command = "INSERT INTO Users (id, name, email, role) VALUES (?, ?, ?, ?)"
            params = (user.id, user.name, user.email, user.role)
        self.DB.execute_command(command, params)

    def get_user(self, user: User) -> User:
        """
        :param user: An incomplete User object. Needs to have the email field, because this is what the function uses to find the rest of the info.
        :return: Either returns a default User object if no match was found, or a complete User object.
        """
        command = "SELECT * FROM Users WHERE email = ? LIMIT 1"
        params = (user.email,)
        result = self.DB.get_one(command, params)

        if result:
            return User.from_row(result)
        else:
            return User()

    def get_users_by_role(self, role: str) -> list[User]:
        """
        :param role: See User.ROLES for a list of allowed roles.
        :return: A list of User objects with a given role.
        """
        if role not in User.ROLES:
            warnings.warn("Invalid role detected. Check spelling!")

        command = "SELECT id, name, email, role FROM Users WHERE role = ?"
        params = (role,)
        result = self.DB.get_all(command, params)
        return [User.from_row(row) for row in result]

    def remove_user(self, user:User):
        """
        If the User passed to this function is the last user of its role, it will not be removed.
        :param user: The User object to be removed.
        :return: None.
        """
        if len(self.get_users_by_role(user.role)) <= 1:
            return
        else:
            command = "DELETE FROM Users WHERE id = ?"
            params = (user.id,)
            self.DB.execute_command(command, params)

    def edit_user(self, user:User):
        """
        :param user: An incomplete User object, with the fields that aren't initialized to defaults corresponding to attributes to update.
        :return: None
        """
        updates = []
        params = []

        if user.name != "Anonymous":
            updates.append("name = ?")
            params.append(user.name)
        if user.email is not None:
            updates.append("email = ?")
            params.append(user.email)
        if user.role is not None:
            updates.append("role = ?")
            params.append(user.role)

        if not updates:
            return

        params.append(user.id)
        command = f"UPDATE Users SET {', '.join(updates)} WHERE id = ?"
        self.DB.execute_command(command, params)