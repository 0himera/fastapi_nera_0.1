from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from core.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.email.MAIL_USERNAME,
    MAIL_PASSWORD=settings.email.MAIL_PASSWORD,
    MAIL_FROM=settings.email.MAIL_FROM,
    MAIL_PORT=settings.email.MAIL_PORT,
    MAIL_SERVER=settings.email.MAIL_SERVER,
    MAIL_STARTTLS=settings.email.MAIL_TLS,  # Используйте MAIL_STARTTLS вместо MAIL_TLS
    MAIL_SSL_TLS=settings.email.MAIL_SSL,  # Используйте MAIL_SSL_TLS вместо MAIL_SSL
    USE_CREDENTIALS=settings.email.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.email.VALIDATE_CERTS,
)


async def send_verification_email(email: str, token: str):
    verification_link = f"{settings.frontend_url}/verify?token={token}"
    message = MessageSchema(
        subject="Confirm your email",
        recipients=[email],
        body=f'Click the link to verify your email: <a href="{verification_link}">Verify Email</a>',
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_reset_password_email(email: str, token: str):
    reset_url = f"{settings.frontend_url}/api/v1/reset-password?token={token}"
    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email],
        body=f"""
        Hello,

        You have requested to reset your password. Click the link below to set a new password:

        {reset_url}

        If you did not request this change, please ignore this email.

        Thank you!
        """,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)