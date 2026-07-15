from email.message import EmailMessage
from pathlib import Path

import aiosmtplib
# from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from backend.config import settings

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

# templates = Jinja2Templates(directory= "templates")
jinja_env = Environment(loader =FileSystemLoader(str(TEMPLATE_DIR)))

# Send Email Functionality
async def send_email(
        to_email: str,
        subject: str,
        plain_text: str,
        html_content: str | None = None,
) -> None:
    message = EmailMessage()
    message["From"] = settings.mail_from
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(plain_text)

    if html_content:
        message.add_alternative(html_content, subtype = "html")
    
    await aiosmtplib.send(
        message,
        hostname = settings.mail_server,
        port = settings.mail_port,
        username = settings.mail_username if settings.mail_username else None,
        password = settings.mail_password.get_secret_value() or None,
        start_tls = settings.mail_use_tls,
    )
async def send_password_reset_email(to_email:str, username: str, token:str) -> None:
    reset_url = f"{settings.frontend_url}/reset-password?token={token}"
    template = jinja_env.get_template("email/password_reset.html")
    html_content = template.render(reset_url=reset_url, username=username)
    plain_text = f"""Hi {username},
Your password Reset is Here. Click Below to Reset Password:
{reset_url}
This link will expire in 1 hour.

If you didn't request this, you can safely ignore this email.
Best regards, 
WealthM
"""
    await send_email(
        to_email=to_email,
        subject="Reset your Password - WealthM",
        plain_text=plain_text,
        html_content=html_content,
    )
 


    
