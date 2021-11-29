from typing import List
from fastapi import Depends, Security, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlmodel import Session
from database import get_db
from helpers.responses import default_responses
from models.session import SessionCreate, SessionRead, SessionUpdate
from models.user import UserSession
from services.session import SessionService
from helpers.security import get_user

_prefix = '/sessions'

router = InferringRouter(
    tags=['Sessions'],
    responses=default_responses
)

# Scopes
_read = ['session.read', 'session.*']
_write = ['session.write', 'session.*']
_update = ['session.update', 'session.*']
_delete = ['session.delete', 'session.*']


@cbv(router)
class SessionRouter:
    db: Session = Depends(get_db)

    @router.get(_prefix + "/")
    async def get_sessions(self, user_session: UserSession = Security(get_user, scopes=_read)) -> List[SessionRead]:
        return await SessionService(user_session, self.db).get_sessions()

    @router.get(_prefix + "/{id}")
    async def get_session(self, id: int, user_session: UserSession = Security(get_user, scopes=_read)) -> SessionRead:
        return await SessionService(user_session, self.db).get_session(id)

    @router.post(_prefix + "/", status_code=status.HTTP_201_CREATED)
    async def create_session(self, session: SessionCreate, user_session: UserSession = Security(get_user, scopes=_write)) -> SessionRead:
        return await SessionService(user_session, self.db).create_session(session)

    @router.patch(_prefix + "/{id}")
    async def update_session(self, id: int, session: SessionUpdate, user_session: UserSession = Security(get_user, scopes=_update)) -> SessionRead:
        return await SessionService(user_session, self.db).update_session(id, session)

    @router.delete(_prefix + "/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_session(self, id: int, user_session: UserSession = Security(get_user, scopes=_delete)):
        return await SessionService(user_session, self.db).delete_session(id)
