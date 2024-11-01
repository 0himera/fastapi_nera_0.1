import uuid

from fastapi_users import FastAPIUsers

from .backend import authentication_backend
from .user_manager import get_user_manager
from core.models.user import User
from core.types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)
