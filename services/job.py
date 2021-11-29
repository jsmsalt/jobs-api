from typing import List
from sqlmodel import Session, or_
from models.job import Job, JobCreate, JobRead, JobUpdate
from models.user import User, UserSession
from services.base import BaseService
from helpers.exceptions import ApiException
from repositories.job import JobRepository
from repositories.user import UserRepository


class JobService(BaseService):

    def __init__(self, user_session: UserSession, db: Session):
        super().__init__(user_session, db)
        self.job_repository = JobRepository(db)
        self.user_repository = UserRepository(db)

    async def get_job(self, job_id) -> JobRead:
        try:
            job = self.job_repository.get_entity(Job.id == job_id)

            if job is None:
                raise ApiException(
                    f'Job with id {job_id} not found')

            return job

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(f'Job with id {job_id} not found')

    async def get_jobs(self) -> List[JobRead]:
        try:
            jobs = self.job_repository.get_entities()

            return jobs
        except Exception:
            raise ApiException('No jobs found')

    async def create_job(self, job: JobCreate) -> JobRead:
        try:
            job: Job = self.job_repository.create_entity(job)

            job.user = self.user_repository.get_entity(
                User.id == self.user_session.user_id)

            self.job_repository.update_entity_changes(job)

            return job

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException('Error creating job')

    async def update_job(self, job_id, job: JobUpdate) -> JobRead:
        try:
            job = self.job_repository.update_entity(job, Job.id == job_id)

            return job

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(
                f'Error updating job with id {job_id}')

    async def delete_job(self, job_id) -> None:
        try:
            result = self.job_repository.delete_entity(
                Job.id == job_id)

            if not result:
                raise ApiException(
                    f'Error deleting job with id {job_id}')

        except ApiException as e:
            raise e
        except Exception:
            raise ApiException(
                f'Error deleting job with id {job_id}')
