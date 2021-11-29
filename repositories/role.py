from repositories.base import BaseRepository
from models.role import Role, RoleCreate, RoleUpdate


class RoleRepository(BaseRepository[Role, RoleCreate, RoleUpdate]):
    entity = Role
