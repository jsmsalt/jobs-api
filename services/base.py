from logger import logger
from fastapi import Response, status, HTTPException
from helpers.exceptions import ApiException, AuthenticationException, AuthorizationException
from models.user import UserSession
from sqlmodel import Session


class BaseService:
    def __init__(self, user_session: UserSession, db: Session):
        self.user_session = user_session
        self.db = db

    def __getattribute__(self, attr):
        attribute = super().__getattribute__(attr)

        if callable(attribute):
            class_name = object.__getattribute__(self, "__class__").__name__
            method_name = str(attr)

            async def wrapper_func(*args, **kwargs):
                private_or_protected = method_name.startswith(
                    "__") or method_name.startswith("_")

                if not private_or_protected:
                    logger.debug(f"{class_name}.{method_name}()")

                try:
                    response = await attribute(*args, **kwargs)

                    if response is None:
                        if private_or_protected:
                            return None
                        else:
                            return Response(status_code=status.HTTP_204_NO_CONTENT)
                    else:
                        return response

                except ApiException as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

                except AuthenticationException as e:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

                except AuthorizationException as e:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

                except Exception as e:
                    logger.error(f"{class_name}.{method_name} failed with {e}")

                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=str(e))

            return wrapper_func

        return attribute
