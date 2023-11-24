from email.mime.text import MIMEText
from smtplib import SMTP
from ssl import create_default_context

from pydantic import BaseModel

from src.core.config import settings


class MailBody(BaseModel):
    to: list[str]
    subject: str
    body: str


def send_mail(data: dict | None = None):
    msg = MailBody(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = settings.smtp_username
    message["To"] = ",".join(msg.to)
    message["Subject"] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}
