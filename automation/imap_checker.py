import imaplib
import email
from email.utils import parsedate_to_datetime
from config import IMAP_HOST, IMAP_PORT, IMAP_USER, IMAP_PASS


def get_reply_dates(leads: list[dict]) -> dict[str, str]:
    """
    Sprawdza IMAP czy leadzi odpisali po dacie wysłania maila.
    Zwraca {email: 'YYYY-MM-DD'} dla tych, którzy odpisali.
    """
    if not leads:
        return {}

    replied = {}

    with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) as mail:
        mail.login(IMAP_USER, IMAP_PASS)
        mail.select("INBOX")

        for lead in leads:
            lead_email = lead["email"]
            sent_date = lead.get("sent_date", "")

            # Szukaj maili od tego adresu, po dacie wysłania
            criteria = f'FROM "{lead_email}"'
            if sent_date:
                # IMAP format daty: DD-Mon-YYYY
                try:
                    from datetime import date
                    d = date.fromisoformat(sent_date)
                    month_abbr = d.strftime("%d-%b-%Y")
                    criteria = f'FROM "{lead_email}" SINCE {month_abbr}'
                except ValueError:
                    pass

            _, data = mail.search(None, criteria)
            if not data or not data[0]:
                continue

            msg_ids = data[0].split()
            if not msg_ids:
                continue

            # Weź najnowszy mail
            _, msg_data = mail.fetch(msg_ids[-1], "(RFC822)")
            if not msg_data or not msg_data[0]:
                continue

            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)

            try:
                dt = parsedate_to_datetime(msg.get("Date", ""))
                replied[lead_email] = dt.date().isoformat()
            except Exception:
                replied[lead_email] = sent_date  # fallback: dzisiejsza data przy ozn.

    return replied
