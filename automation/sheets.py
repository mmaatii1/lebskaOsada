import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_ID, SHEET_NAME

_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Kolumny w arkuszu (1-based)
COL_NAME = 1    # A: Imię
COL_EMAIL = 2   # B: Email
COL_SENT = 3    # C: Wysłano (data)
COL_REPLIED = 4 # D: Odpisano (data)


def _get_sheet():
    creds = Credentials.from_service_account_file("credentials.json", scopes=_SCOPES)
    gc = gspread.authorize(creds)
    return gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


def get_unsent_leads():
    sheet = _get_sheet()
    rows = sheet.get_all_records()
    leads = []
    for i, row in enumerate(rows, start=2):  # start=2 bo wiersz 1 to nagłówek
        if row.get("Email") and not row.get("Wysłano"):
            leads.append({
                "row": i,
                "name": row.get("Imię", ""),
                "email": row["Email"],
            })
    return leads


def get_pending_reply_leads():
    sheet = _get_sheet()
    rows = sheet.get_all_records()
    pending = []
    for i, row in enumerate(rows, start=2):
        if row.get("Wysłano") and not row.get("Odpisano"):
            pending.append({
                "row": i,
                "email": row["Email"],
                "sent_date": row["Wysłano"],
            })
    return pending


def mark_sent(row_num: int, sent_date: str):
    sheet = _get_sheet()
    sheet.update_cell(row_num, COL_SENT, sent_date)


def mark_replied(row_num: int, reply_date: str):
    sheet = _get_sheet()
    sheet.update_cell(row_num, COL_REPLIED, reply_date)
