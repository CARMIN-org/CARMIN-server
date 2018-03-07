from server.database.models.user import User, Role
from werkzeug.security import generate_password_hash


def admin(encrypted=False):
    return User(
        username="admin",
        password=generate_password_hash("admin") if encrypted else "admin",
        role=Role.admin,
        api_key="admin-api-key")


def standard_user(encrypted=False):
    return User(
        username="user",
        password=generate_password_hash("user") if encrypted else "user",
        role=Role.user,
        api_key="standard-user-api-key")


def standard_user_2(encrypted=False):
    return User(
        username="user2",
        password=generate_password_hash("user2") if encrypted else "user",
        role=Role.user,
        api_key="standard-user-2-api-key")
