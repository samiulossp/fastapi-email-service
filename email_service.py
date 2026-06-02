from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SENDER_NAME, SENDER_EMAIL
from typing import List, Optional

# Validate configuration
if not SMTP_USER or not SMTP_PASS:
    raise ValueError(
        "Missing email configuration. Please set SMTP_USER and SMTP_PASSWORD in .env file\n"
        "Example .env file:\n"
        "SMTP_HOST=smtp.gmail.com\n"
        "SMTP_PORT=587\n"
        "SMTP_USER=your-email@gmail.com\n"
        "SMTP_PASSWORD=your-16-character-app-password\n"
        "SENDER_NAME=Your Name\n"
        "SENDER_EMAIL=your-email@gmail.com"
    )

# Configure email connection
conf = ConnectionConfig(
    MAIL_SERVER=SMTP_HOST,
    MAIL_PORT=SMTP_PORT,
    MAIL_USERNAME=SMTP_USER,
    MAIL_PASSWORD=SMTP_PASS,
    MAIL_FROM=SENDER_EMAIL,
    MAIL_FROM_NAME=SENDER_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

fast_mail = FastMail(conf)

async def send_email(
    subject: str,
    recipients: List[str],
    body: str,
    html_body: str = None,
    cc: Optional[List[str]] = None,
) -> tuple[bool, str]:
    try:
        if not recipients:
            return False, "No recipients specified"
        
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            cc=cc,
            body=body,
            subtype="html" if html_body else "plain",
            html=html_body,
        )
        await fast_mail.send_message(message)
        return True, "Email sent successfully"
    except Exception as e:
        error_msg = f"Error sending email: {str(e)}"
        print(error_msg)
        return False, error_msg
