from typing import List
from models import User

_fake_db = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
]

class UserRepository:
    def get_all(self) -> List[User]:
        return _fake_db

    def get_by_id(self, user_id: int) -> User | None:
        return next((user for user in _fake_db if user.id == user_id), None)
