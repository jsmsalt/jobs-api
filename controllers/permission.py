from typing import List
from fastapi import Depends, Security, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlmodel import Session
from database import get_db
from helpers.responses import default_responses
from models.permission import PermissionCreate, PermissionRead, PermissionUpdate
from services.permission import PermissionService
from helpers.security import get_user
from models.user import UserSession

_prefix = '/permissions'

router = InferringRouter(
    tags=['Permissions'],
    responses=default_responses
)

# Scopes
_read = ['permission.read', 'permission.*']
_write = ['permission.write', 'permission.*']
_update = ['permission.update', 'permission.*']
_delete = ['permission.delete', 'permission.*']


@cbv(router)
class PermissionRouter:
    db: Session = Depends(get_db)

    @router.get(_prefix + "/")
    async def get_permissions(self, user_session: UserSession = Security(get_user, scopes=_read)) -> List[PermissionRead]:
        return await PermissionService(user_session, self.db).get_permissions()

    @router.get(_prefix + "/{id}")
    async def get_permission(self, id: int, user_session: UserSession = Security(get_user, scopes=_read)) -> PermissionRead:
        return await PermissionService(user_session, self.db).get_permission(id)

    @router.post(_prefix + "/", status_code=status.HTTP_201_CREATED)
    async def create_permission(self, permission: PermissionCreate, user_session: UserSession = Security(get_user, scopes=_write)) -> PermissionRead:
        return await PermissionService(user_session, self.db).create_permission(permission)

    @router.patch(_prefix + "/{id}")
    async def update_permission(self, id: int, permission: PermissionUpdate, user_session: UserSession = Security(get_user, scopes=_update)) -> PermissionRead:
        return await PermissionService(user_session, self.db).update_permission(id, permission)

    @router.delete(_prefix + "/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_permission(self, id: int, user_session: UserSession = Security(get_user, scopes=_delete)):
        return await PermissionService(user_session, self.db).delete_permission(id)
