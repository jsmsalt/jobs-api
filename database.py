import sys
from sqlalchemy.engine.url import make_url
from sqlmodel import SQLModel, create_engine, Session
from settings import Settings

import models.permission_role
import models.permission
import models.role
import models.session
import models.job
import models.user

settings = Settings()

if "pytest" in sys.modules:
    db_uri = settings.db_uri_test
else:
    db_uri = settings.db_uri

engine = create_engine(
    make_url(db_uri),
    echo=False,
    connect_args={'check_same_thread': False}
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
