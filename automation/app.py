"""
Webhook server — uruchom na serwerze:
  python app.py

Google Apps Script wysyła POST /webhook gdy pojawi się nowy lead.
"""
import datetime
import logging
from flask import Flask, request, jsonify
from config import WEBHOOK_SECRET
from sheets import mark_sent
from mailer import send_offer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    secret = request.headers.get("X-Secret", "")
    if secret != WEBHOOK_SECRET:
        log.warning("Nieautoryzowane żądanie webhooka")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    name = data.get("name", "")
    lead_email = data.get("email", "")
    row = data.get("row")

    if not lead_email or not row:
        return jsonify({"error": "Brakuje email lub row"}), 400

    try:
        send_offer(lead_email, name)
        mark_sent(row, datetime.date.today().isoformat())
        log.info("Wysłano ofertę do %s (wiersz %s)", lead_email, row)
        return jsonify({"status": "ok"})
    except Exception as exc:
        log.error("Błąd wysyłki do %s: %s", lead_email, exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
