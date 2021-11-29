from repositories.base import BaseRepository
from models.user import User, UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    entity = User
