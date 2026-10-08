import base64

from googleapiclient.discovery import build

from .auth import get_gmail_credentials


def get_gmail_service():
    """
    Create and return an authenticated Gmail API service.
    """

    credentials = get_gmail_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    return service


def get_latest_emails(max_results=5):
    """
    Fetch the latest emails from Gmail.
    """

    service = get_gmail_service()

    response = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])

    emails = []

    for message in messages:

        email_data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        emails.append(parse_email(email_data))

    return emails


def parse_email(email_data):
    """
    Extract useful information from a Gmail message.
    """

    headers = email_data["payload"].get("headers", [])

    sender = ""
    subject = ""
    date = ""

    for header in headers:

        name = header["name"].lower()
        value = header["value"]

        if name == "from":
            sender = value

        elif name == "subject":
            subject = value

        elif name == "date":
            date = value

    body = extract_body(email_data["payload"])

    return {
        "id": email_data["id"],
        "sender": sender,
        "subject": subject,
        "date": date,
        "body": body
    }


def extract_body(payload):
    """
    Extract plain-text email body.
    """

    # Simple email
    if payload.get("body", {}).get("data"):

        data = payload["body"]["data"]

        return base64.urlsafe_b64decode(data).decode(
            "utf-8",
            errors="ignore"
        )

    # Multipart email
    parts = payload.get("parts", [])

    for part in parts:

        if part["mimeType"] == "text/plain":

            data = part["body"].get("data")

            if data:
                return base64.urlsafe_b64decode(data).decode(
                    "utf-8",
                    errors="ignore"
                )

    return ""