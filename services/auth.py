from sqlmodel import Session
from helpers.security import encode_token
from models.session import SessionCreate, SessionUpdate
from models.user import AccessToken, User, UserCredentials, UserSession
from models.session import Session as SessionModel
from repositories.user import UserRepository
from repositories.session import SessionRepository
from services.base import BaseService
from helpers.exceptions import ApiException, AuthenticationException
from helpers.password import verify_password


class AuthService(BaseService):

    def __init__(self, user_session: UserSession, db: Session):
        super().__init__(user_session, db)
        self.user_repository = UserRepository(db)
        self.session_repository = SessionRepository(db)

    async def user_login(self, credentials: UserCredentials) -> AccessToken:
        try:
            user = self.user_repository.get_entity(
                User.username == credentials.username)

            if not user:
                raise AuthenticationException('Wrong username or password')

            if not user.is_active:
                raise AuthenticationException('User is not active')

            if not verify_password(credentials.password, user.password):
                raise AuthenticationException('Wrong username or password')

            permissions = [p.name for p in user.role.permissions]

            # Create access token
            token = encode_token(
                UserSession(
                    user_id=user.id,
                    role=user.role.name,
                    permissions=permissions
                )
            )

            # Invalidate old sessions
            self.session_repository.update_entities(
                SessionUpdate(
                    is_active=False
                ),
                SessionModel.user_id == user.id, SessionModel.is_active == True
            )

            # Create new session
            self.session_repository.create_entity(SessionCreate(
                access_token=token,
                user_id=user.id
            ))

            return AccessToken(
                access_token=token,
                token_type='Bearer'
            )

        except AuthenticationException as e:
            raise e
        except Exception:
            raise AuthenticationException('Wrong username or password')

    async def user_logout(self) -> None:
        try:
            # Invalidate old sessions
            self.session_repository.update_entities(
                SessionUpdate(
                    is_active=False
                ),
                SessionModel.user_id == self.user_session.user_id, SessionModel.is_active == True
            )

            return None
        except Exception:
            raise ApiException('Error while logging out')
