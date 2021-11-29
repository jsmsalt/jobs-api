from repositories.base import BaseRepository
from models.session import Session, SessionCreate, SessionUpdate


class SessionRepository(BaseRepository[Session, SessionCreate, SessionUpdate]):
    entity = Session
