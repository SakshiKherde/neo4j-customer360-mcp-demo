import os
from datetime import datetime
from typing import Dict

import resend

from src.utils.logger import get_logger

logger = get_logger(__name__)


def send_via_resend(html: str, content: Dict, config: dict):
    resend.api_key = os.environ.get("RESEND_API_KEY")

    email_cfg = config.get("email", {})
    newsletter_cfg = config.get("newsletter", {})

    today = datetime.now().strftime("%B %d, %Y")
    subject = f"The Daily Brief \u2014 {today}"

    recipient = os.environ.get(
        "NEWSLETTER_RECIPIENT",
        newsletter_cfg.get("recipient_email", ""),
    )

    if not recipient:
        raise ValueError("No recipient email configured. Set NEWSLETTER_RECIPIENT or newsletter.recipient_email in config.yaml")

    params: resend.Emails.SendParams = {
        "from": f"{email_cfg.get('from_name', 'The Daily Brief')} <{email_cfg.get('from_address', 'brief@yourdomain.com')}>",
        "to": [recipient],
        "subject": subject,
        "html": html,
    }

    response = resend.Emails.send(params)
    logger.info(f"Email sent via Resend to {recipient} | id={response.get('id', 'unknown')}")
    return response


def send_newsletter(html: str, content: Dict, config: dict):
    provider = config.get("email", {}).get("provider", "resend")

    if provider == "resend":
        send_via_resend(html, content, config)
    else:
        raise ValueError(
            f"Unknown email provider '{provider}'. "
            "Supported: resend. (Gmail support coming in V2.)"
        )
