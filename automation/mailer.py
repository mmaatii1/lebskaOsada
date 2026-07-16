import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL, FROM_NAME

SUBJECT = "Oferta apartamentu — Łebska Osada, Żarnowska k. Łeby"

# ── szablon HTML ──────────────────────────────────────────────────────────────
_HTML = """\
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body {{ margin:0; padding:0; background:#eaf6fd; font-family:'DM Sans',Arial,sans-serif; color:#154360; }}
  .wrap {{ max-width:600px; margin:32px auto; background:#f0f9ff; border-radius:12px; overflow:hidden; box-shadow:0 4px 24px rgba(21,67,96,.12); }}
  .header {{ background:#1a5276; padding:36px 40px 28px; text-align:center; }}
  .header h1 {{ margin:0; color:#c09a52; font-size:26px; font-family:Georgia,serif; letter-spacing:.5px; }}
  .header p  {{ margin:6px 0 0; color:#d6eaf8; font-size:13px; letter-spacing:1px; text-transform:uppercase; }}
  .body {{ padding:36px 40px; }}
  .body p {{ line-height:1.7; margin:0 0 16px; }}
  .highlights {{ background:#d6eaf8; border-radius:8px; padding:20px 24px; margin:24px 0; }}
  .highlights ul {{ margin:0; padding-left:20px; }}
  .highlights li {{ margin-bottom:8px; }}
  .cta {{ text-align:center; margin:32px 0 16px; }}
  .btn {{ display:inline-block; background:#c09a52; color:#fff; text-decoration:none;
          padding:14px 36px; border-radius:6px; font-weight:700; font-size:15px; letter-spacing:.3px; }}
  .footer {{ background:#1a5276; color:#5d8aa8; font-size:12px; text-align:center; padding:20px 40px; }}
  .footer a {{ color:#5dade2; text-decoration:none; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <h1>Łebska Osada</h1>
    <p>Luksusowe apartamenty — Żarnowska k. Łeby</p>
  </div>
  <div class="body">
    <p>Szanowny/-a <strong>{name}</strong>,</p>
    <p>
      Dziękujemy za zainteresowanie inwestycją w apartamenty <strong>Łebska Osada</strong>.
      Z przyjemnością przedstawiamy Państwu naszą aktualną ofertę.
    </p>
    <div class="highlights">
      <ul>
        <li>Lokalizacja 200 m od plaży w Żarnowskiej k. Łeby</li>
        <li>Apartamenty 2- i 3-pokojowe (37–62 m²)</li>
        <li>Wysoki standard wykończenia &amp; taras/balkon</li>
        <li>Możliwość przystąpienia do programu najmu wakacyjnego</li>
        <li>Atrakcyjne warunki płatności &amp; rabaty dla pierwszych nabywców</li>
      </ul>
    </div>
    <p>
      Chętnie umówimy się na rozmowę lub prezentację projektu — zarówno online, jak i stacjonarnie.
    </p>
    <div class="cta">
      <a href="https://lebskaosada.pl/" class="btn">Zobacz ofertę na stronie</a>
    </div>
    <p>
      W razie pytań prosimy o kontakt — odpiszemy niezwłocznie.
    </p>
    <p>Z poważaniem,<br>
    <strong>Patrycja Leonowicz</strong><br>
    Doradca ds. Sprzedaży | Łebska Osada<br>
    Tel.: <a href="tel:+48792503213">+48 792 503 213</a>
    </p>
  </div>
  <div class="footer">
    ul. Wydmowa, Żarnowska 84-360, Pomorskie &nbsp;|&nbsp;
    <a href="mailto:sprzedaz@lebskaosada.pl">sprzedaz@lebskaosada.pl</a><br>
    <a href="https://lebskaosada.pl/">lebskaosada.pl</a>
  </div>
</div>
</body>
</html>
"""


def send_offer(to_email: str, to_name: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email

    msg.attach(MIMEText(_HTML.format(name=to_name or "Państwo"), "html", "utf-8"))

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as srv:
        srv.login(SMTP_USER, SMTP_PASS)
        srv.sendmail(FROM_EMAIL, to_email, msg.as_string())
