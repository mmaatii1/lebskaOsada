"""
Uruchamiaj przez cron, np. co 2h:
  0 */2 * * * cd /path/to/automation && python check_replies.py >> /var/log/lebska_replies.log 2>&1
"""
import logging
from sheets import get_pending_reply_leads, mark_replied
from imap_checker import get_reply_dates

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def main():
    pending = get_pending_reply_leads()
    if not pending:
        log.info("Brak leadów oczekujących na odpowiedź")
        return

    log.info("Sprawdzam %d leadów pod kątem odpowiedzi...", len(pending))
    replied = get_reply_dates(pending)

    for lead in pending:
        email = lead["email"]
        if email in replied:
            mark_replied(lead["row"], replied[email])
            log.info("Odpisał: %s (%s)", email, replied[email])

    log.info("Gotowe. Znaleziono %d odpowiedzi.", len(replied))


if __name__ == "__main__":
    main()
