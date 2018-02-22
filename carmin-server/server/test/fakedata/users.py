from server.database.models.user import User, Role


def admin():
    return User(
        username="admin",
        password="admin",
        role=Role.admin,
        api_key="admin-api-key")


def standard_user():
    return User(
        username="user",
        password="user",
        role=Role.user,
        api_key="standard-user-api-key")
