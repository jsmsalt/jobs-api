import jwt
from settings import Settings
from datetime import timedelta, datetime
from fastapi import HTTPException, status, Security, Depends
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session
from database import get_db

from models.user import UserSession
from models.session import Session as SessionModel
from repositories.session import SessionRepository


security = HTTPBearer(auto_error=False)


def encode_token(session: UserSession, expire_delta: timedelta = timedelta(days=365)) -> str:
    """Create JSON Web Token"""

    expire = datetime.utcnow() + expire_delta

    token_data = {
        'sub': session.user_id,
        'role': session.role or "",
        'permissions': session.permissions or [],
        'exp': expire,
    }

    settings = Settings()

    jwt_token = jwt.encode(token_data, settings.jwt_secret,
                           algorithm=settings.jwt_algorithm)

    return jwt_token


def decode_token(jwt_token: str) -> dict:
    """Decode a JSON Web Token"""

    settings = Settings()
    return jwt.decode(jwt_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


async def get_user(security_scopes: SecurityScopes,
                   auth: HTTPAuthorizationCredentials = Security(security),
                   db: Session = Depends(get_db)) -> UserSession:
    """Validate and return the user in the JSON Web Token."""

    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication rejected, invalid token')

    try:
        payload = decode_token(auth.credentials)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication rejected, invalid token')
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication rejected, invalid token')

    # Verify that the user has the required scopes for this endpoint
    permissions = payload.get('permissions', [])
    role = payload.get('role', '')

    permissions_dict = {}

    for permission in permissions:
        permission_action = permission.split('.')

        if len(permission_action) == 2:
            if permission_action[0] in permissions_dict:
                permissions_dict[permission_action[0]].append(
                    permission_action[1])
            else:
                permissions_dict[permission_action[0]] = [permission_action[1]]

    scopes_dict = {}

    for scope in security_scopes.scopes:
        scope_action = scope.split('.')

        if len(scope_action) == 2:
            if scope_action[0] in scopes_dict:
                scopes_dict[scope_action[0]].append(
                    scope_action[1])
            else:
                scopes_dict[scope_action[0]] = [scope_action[1]]

    for entity, actions in scopes_dict.items():
        if entity not in permissions_dict:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Access denied, you do not have the required permissions'
            )
        else:
            for action in permissions_dict[entity]:
                if action not in actions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='Access denied, you do not have the required permissions'
                    )

    user_id = payload.get('sub')

    # Check if the user is active and if has active tokens

    # TODO: <Add Redis Cache>
    session_repository = SessionRepository(db)

    session = session_repository.get_entity(
        SessionModel.access_token == auth.credentials,
        SessionModel.user_id == user_id,
        SessionModel.is_active == True
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication rejected, invalid token'
        )

    user = session.user

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication rejected, invalid token'
        )

    # TODO: </Add Redis Cache>

    try:
        return UserSession(
            user_id=user_id,
            role=role,
            permissions=permissions
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied, you do not have the required permissions')
