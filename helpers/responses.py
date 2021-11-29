
from fastapi import status

from schemas.error import ErrorSchema


default_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        'description': 'Authentication Error',
        'model': ErrorSchema
    },
    status.HTTP_403_FORBIDDEN: {
        'description': 'Permissions Error',
        'model': ErrorSchema
    }
}
