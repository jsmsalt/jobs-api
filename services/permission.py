from typing import List
from sqlmodel import Session
from models.permission import Permission, PermissionCreate, PermissionRead, PermissionUpdate
from models.user import UserSession
from services.base import BaseService
from helpers.exceptions import ApiException
from repositories.permission import PermissionRepository


class PermissionService(BaseService):

    def __init__(self, user_session: UserSession, db: Session):
        super().__init__(user_session, db)
        self.permission_repository = PermissionRepository(db)

    async def get_permission(self, permission_id) -> PermissionRead:
        try:
            permission = self.permission_repository.get_entity(
                Permission.id == permission_id)

            if permission is None:
                raise ApiException(
                    f'Permission with id {permission_id} not found')

            return permission

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(f'Permission with id {permission_id} not found')

    async def get_permissions(self) -> List[PermissionRead]:
        try:
            permissions = self.permission_repository.get_entities()

            return permissions
        except Exception:
            raise ApiException('No permissions found')

    async def create_permission(self, permission: PermissionCreate) -> PermissionRead:
        try:
            permission_exists = self.permission_repository.get_entity(
                Permission.name == permission.name)

            if permission_exists is not None:
                raise ApiException('Permission already exists')

            permission = self.permission_repository.create_entity(permission)

            return permission

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException('Error creating permission')

    async def update_permission(self, permission_id, permission: PermissionUpdate) -> PermissionRead:
        try:
            if permission.name is not None:
                permission_exists = self.permission_repository.get_entity(
                    Permission.name == permission.name)

                if permission_exists is not None:
                    raise ApiException('Permission already exists')

            permission = self.permission_repository.update_entity(
                permission, Permission.id == permission_id)

            return permission

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(
                f'Error updating permission with id {permission_id}')

    async def delete_permission(self, permission_id) -> None:
        try:
            result = self.permission_repository.delete_entity(
                Permission.id == permission_id)

            if not result:
                raise ApiException(
                    f'Error deleting permission with id {permission_id}')

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(
                f'Error deleting permission with id {permission_id}')
