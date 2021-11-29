from typing import List
from sqlmodel import Session
from models.session import Session as SessionModel, SessionCreate, SessionRead, SessionUpdate
from models.user import UserSession
from services.base import BaseService
from helpers.exceptions import ApiException
from repositories.session import SessionRepository


class SessionService(BaseService):

    def __init__(self, user_session: UserSession, db: Session):
        super().__init__(user_session, db)
        self.session_repository = SessionRepository(db)

    async def get_session(self, session_id) -> SessionRead:
        try:
            session = self.session_repository.get_entity(
                SessionModel.id == session_id)

            if session is None:
                raise ApiException(
                    f'Session with id {session_id} not found')

            return session

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(f'Session with id {session_id} not found')

    async def get_sessions(self) -> List[SessionRead]:
        try:
            sessions = self.session_repository.get_entities()

            return sessions
        except Exception:
            raise ApiException('No sessions found')

    async def create_session(self, session: SessionCreate) -> SessionRead:
        try:
            session = self.session_repository.create_entity(session)

            return session
        except Exception:
            raise ApiException('Error creating session')

    async def update_session(self, session_id, session: SessionUpdate) -> SessionRead:
        try:
            session = self.session_repository.update_entity(
                session, SessionModel.id == session_id)

            return session
        except Exception:
            raise ApiException(
                f'Error updating session with id {session_id}')

    async def delete_session(self, session_id) -> None:
        try:
            result = self.session_repository.delete_entity(
                SessionModel.id == session_id)

            if not result:
                raise ApiException(
                    f'Error deleting session with id {session_id}')

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(
                f'Error deleting session with id {session_id}')
