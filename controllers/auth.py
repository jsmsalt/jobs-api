from fastapi import Depends, Security, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlmodel import Session
from database import get_db
from helpers.responses import default_responses
from models.user import AccessToken, UserCredentials
from services.auth import AuthService
from helpers.security import get_user
from models.user import UserSession

_prefix = '/auth'

router = InferringRouter(
    tags=['Auth'],
    responses=default_responses
)


@cbv(router)
class AuthRouter:
    db: Session = Depends(get_db)

    @router.post(_prefix + "/login")
    async def login(self, credentials: UserCredentials) -> AccessToken:
        return await AuthService(None, self.db).user_login(credentials)

    @router.post(_prefix + "/logout", status_code=status.HTTP_204_NO_CONTENT)
    async def logout(self, user_session: UserSession = Security(get_user, scopes=[])):
        return await AuthService(user_session, self.db).user_logout()
