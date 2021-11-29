from typing import List
from fastapi import Depends, Security, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlmodel import Session
from database import get_db
from helpers.responses import default_responses
from models.user import UserCreate, UserRead, UserSession, UserUpdate
from services.user import UserService
from helpers.security import get_user

router = InferringRouter(
    tags=['Users'],
    responses=default_responses
)

# Scopes
_read = ['user.read', 'user.*']
_write = ['user.write', 'user.*']
_update = ['user.update', 'user.*']
_delete = ['user.delete', 'user.*']


@cbv(router)
class UserRouter:
    db: Session = Depends(get_db)

    @router.get("/users")
    async def get_users(self, user_session: UserSession = Security(get_user, scopes=_read)) -> List[UserRead]:
        return await UserService(user_session, self.db).get_users()

    @router.post("/users/", status_code=status.HTTP_201_CREATED)
    async def create_user(self, user: UserCreate, user_session: UserSession = Security(get_user, scopes=_write)) -> UserRead:
        return await UserService(user_session, self.db).create_user(user)

    @router.get("/users/{id}")
    async def get_user(self, id: int, user_session: UserSession = Security(get_user, scopes=_read)) -> UserRead:
        return await UserService(user_session, self.db).get_user(id)

    @router.patch("/users/{id}")
    async def update_user(self, id: int, user: UserUpdate, user_session: UserSession = Security(get_user, scopes=_update)) -> UserRead:
        return await UserService(user_session, self.db).update_user(id, user)

    @router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(self, id: int, user_session: UserSession = Security(get_user, scopes=_delete)):
        return await UserService(user_session, self.db).delete_user(id)

    @router.patch("/users/{id}/disable", status_code=status.HTTP_204_NO_CONTENT)
    async def disable_user(self, id: int, user_session: UserSession = Security(get_user, scopes=_update)):
        return await UserService(user_session, self.db).disable_user(id)
