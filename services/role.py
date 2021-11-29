from typing import List
from sqlmodel import Session
from models.role import Role, RoleCreate, RoleRead, RoleUpdate
from models.user import UserSession
from services.base import BaseService
from helpers.exceptions import ApiException
from repositories.role import RoleRepository


class RoleService(BaseService):

    def __init__(self, user_session: UserSession, db: Session):
        super().__init__(user_session, db)
        self.role_repository = RoleRepository(db)

    async def get_role(self, role_id) -> RoleRead:
        try:
            role = self.role_repository.get_entity(Role.id == role_id)

            if role is None:
                raise ApiException(f'Role with id {role_id} not found')

            return role

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(f'Role with id {role_id} not found')

    async def get_roles(self) -> List[RoleRead]:
        try:
            roles = self.role_repository.get_entities()

            return roles
        except Exception:
            raise ApiException('No roles found')

    async def create_role(self, role: RoleCreate) -> RoleRead:
        try:
            role_exists = self.role_repository.get_entity(
                Role.name == role.name)

            if role_exists is not None:
                raise ApiException('Role already exists')

            role = self.role_repository.create_entity(role)

            return role

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException('Error creating role')

    async def update_role(self, role_id, role: RoleUpdate) -> RoleRead:
        try:
            if role.name is not None:
                role_exists = self.role_repository.get_entity(
                    Role.name == role.name)

                if role_exists is not None:
                    raise ApiException('Role already exists')

            role = self.role_repository.update_entity(role, Role.id == role_id)

            return role

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(f'Error updating role with id {role_id}')

    async def delete_role(self, role_id) -> None:
        try:
            result = self.role_repository.delete_entity(Role.id == role_id)

            if not result:
                raise ApiException(f'Error deleting role with id {role_id}')

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(f'Error deleting role with id {role_id}')
