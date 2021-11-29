from typing import List
from fastapi import Depends, Security, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlmodel import Session
from database import get_db
from helpers.responses import default_responses
from models.user import UserSession
from services.job import JobService
from models.job import JobRead, JobUpdate, JobCreate
from helpers.security import get_user

_prefix = "/jobs"

router = InferringRouter(
    tags=['Jobs'],
    responses=default_responses
)

# Scopes
_read = ['job.read', 'job.*']
_write = ['job.write', 'job.*']
_update = ['job.update', 'job.*']
_delete = ['job.delete', 'job.*']


@cbv(router)
class JobRouter:
    db: Session = Depends(get_db)

    @router.get(_prefix + "/{id}")
    async def get_job(self, id: int, user_session: UserSession = Security(get_user, scopes=_read)) -> JobRead:
        return await JobService(user_session, self.db).get_job(id)

    @router.get(_prefix + "/")
    async def get_jobs(self, user_session: UserSession = Security(get_user, scopes=_read)) -> List[JobRead]:
        return await JobService(user_session, self.db).get_jobs()

    @router.post(_prefix + "/", status_code=status.HTTP_201_CREATED)
    async def create_job(self, job: JobCreate, user_session: UserSession = Security(get_user, scopes=_write)) -> JobRead:
        return await JobService(user_session, self.db).create_job(job)

    @router.patch(_prefix + "/{id}")
    async def update_job(self, id: int, job: JobUpdate, user_session: UserSession = Security(get_user, scopes=_update)) -> JobRead:
        return await JobService(user_session, self.db).update_job(id, job)

    @router.delete(_prefix + "/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_job(self, id: int, user_session: UserSession = Security(get_user, scopes=_delete)):
        return await JobService(user_session, self.db).delete_job(id)
