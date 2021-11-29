from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str
    db_uri: str
    db_uri_test: str
    admin_password: str
    version: str

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
