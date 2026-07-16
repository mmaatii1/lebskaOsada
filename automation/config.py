import os
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SHEET_NAME = os.getenv("SHEET_NAME", "Arkusz1")

SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]

IMAP_HOST = os.environ["IMAP_HOST"]
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.environ["IMAP_USER"]
IMAP_PASS = os.environ["IMAP_PASS"]

FROM_EMAIL = os.environ["FROM_EMAIL"]
FROM_NAME = os.getenv("FROM_NAME", "Łebska Osada")

WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
