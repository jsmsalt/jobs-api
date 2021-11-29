from typing import List
from fastapi import Depends, Security, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlmodel import Session
from database import get_db
from helpers.responses import default_responses
from models.role import RoleCreate, RoleRead, RoleUpdate
from models.user import UserSession
from services.role import RoleService
from helpers.security import get_user

_prefix = '/roles'

router = InferringRouter(
    tags=['Roles'],
    responses=default_responses
)

# Scopes
_read = ['role.read', 'role.*']
_write = ['role.write', 'role.*']
_update = ['role.update', 'role.*']
_delete = ['role.delete', 'role.*']


@cbv(router)
class RoleRouter:
    db: Session = Depends(get_db)

    @router.get(_prefix + "/")
    async def get_roles(self, user_session: UserSession = Security(get_user, scopes=_read)) -> List[RoleRead]:
        return await RoleService(user_session, self.db).get_roles()

    @router.get(_prefix + "/{id}")
    async def get_role(self, id: int, user_session: UserSession = Security(get_user, scopes=_read)) -> RoleRead:
        return await RoleService(user_session, self.db).get_role(id)

    @router.post(_prefix + "/", status_code=status.HTTP_201_CREATED)
    async def create_role(self, role: RoleCreate, user_session: UserSession = Security(get_user, scopes=_write)) -> RoleRead:
        return await RoleService(user_session, self.db).create_role(role)

    @router.patch(_prefix + "/{id}")
    async def update_role(self, id: int, role: RoleUpdate, user_session: UserSession = Security(get_user, scopes=_update)) -> RoleRead:
        return await RoleService(user_session, self.db).update_role(id, role)

    @router.delete(_prefix + "/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_role(self, id: int, user_session: UserSession = Security(get_user, scopes=_delete)):
        return await RoleService(user_session, self.db).delete_role(id)
