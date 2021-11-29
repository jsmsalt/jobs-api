from repositories.base import BaseRepository
from models.job import Job, JobCreate, JobUpdate


class JobRepository(BaseRepository[Job, JobCreate, JobUpdate]):
    entity = Job
