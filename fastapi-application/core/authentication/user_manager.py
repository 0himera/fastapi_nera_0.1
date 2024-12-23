import logging
from typing import Optional, TYPE_CHECKING

from api.dependencies.authentication.email_utils import send_verification_email, send_reset_password_email

if TYPE_CHECKING:
    from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from core.config import settings
from core.types.user_id import UserIdType

from core.models.user import User

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )


    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
        log.info("on_after_request_verify method called for user %r", user.id)
        await send_verification_email(user.email, token)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )
        await send_reset_password_email(user.email, token)
