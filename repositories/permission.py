from repositories.base import BaseRepository
from models.permission import Permission, PermissionCreate, PermissionUpdate


class PermissionRepository(BaseRepository[Permission, PermissionCreate, PermissionUpdate]):
    entity = Permission
