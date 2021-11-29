from typing import List
from sqlmodel import Session, or_
from helpers.password import hash_password
from models.role import Role
from models.session import SessionUpdate, Session as SessionModel
from models.user import User, UserCreate, UserRead, UserSession, UserUpdate
from repositories.session import SessionRepository
from repositories.user import UserRepository
from repositories.role import RoleRepository
from services.base import BaseService
from helpers.exceptions import ApiException


class UserService(BaseService):

    def __init__(self, user_session: UserSession, db: Session):
        super().__init__(user_session, db)
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)
        self.session_repository = SessionRepository(db)

    async def get_user(self, user_id) -> UserRead:
        try:
            user = self.user_repository.get_entity(User.id == user_id)

            if user is None:
                raise ApiException(f'User with id {user_id} not found')

            return user

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(f'User with id {user_id} not found')

    async def get_users(self) -> List[UserRead]:
        try:
            users = self.user_repository.get_entities()

            return users
        except Exception:
            raise ApiException('Users not found')

    async def create_user(self, user: UserCreate) -> UserRead:
        try:
            user_exists = self.user_repository.get_entity(
                or_(User.email == user.email, User.username == user.username))

            if user_exists is not None:
                raise ApiException(
                    'User with this username or email already exists')

            role_exists = self.role_repository.get_entity(
                Role.id == user.role_id)

            if role_exists is None:
                raise ApiException(f'Role with id {user.role_id} not found')

            user.password = hash_password(user.password)
            user.role_id = role_exists.id
            user = self.user_repository.create_entity(user)

            return user

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException('Error creating user')

    async def update_user(self, user_id, user: UserUpdate) -> UserRead:
        try:
            if user.email is not None:
                user_exists = self.user_repository.get_entity(
                    User.email == user.email)

                if user_exists is not None and user_exists.id != user_id:
                    raise ApiException('User with this email already exists')

            user = self.user_repository.update_entity(user, User.id == user_id)

            return user

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException('Error updating user')

    async def delete_user(self, user_id) -> None:
        try:
            result = self.user_repository.delete_entity(User.id == user_id)

            if not result:
                raise ApiException(f'User with id {user_id} not found')

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(f'Error deleting user with id {user_id}')

    async def disable_user(self, user_id) -> None:
        try:
            self.user_repository.update_entity(
                UserUpdate(active=False), User.id == user_id)
            self.session_repository.update_entity(SessionUpdate(
                active=False), SessionModel.user_id == user_id)
        except Exception:
            raise ApiException(f'Error disabling user with id {user_id}')
