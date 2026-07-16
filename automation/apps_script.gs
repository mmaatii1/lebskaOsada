// ── Konfiguracja ─────────────────────────────────────────────────────────────
const WEBHOOK_URL    = "https://TWOJ_SERWER:5001/webhook";  // zmień
const WEBHOOK_SECRET = "TWOJ_SEKRET";                        // musi = .env WEBHOOK_SECRET

// Kolumny (1-based)
const COL_NAME    = 1; // A: Imię
const COL_EMAIL   = 2; // B: Email
const COL_SENT    = 3; // C: Wysłano

// ── Trigger: uruchamia się przy każdej edycji arkusza ─────────────────────────
function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const range = e.range;
  const row   = range.getRow();

  // Pomijaj nagłówek
  if (row === 1) return;

  // Reaguj tylko gdy edytowana jest kolumna Email (B)
  if (range.getColumn() !== COL_EMAIL) return;

  const name      = sheet.getRange(row, COL_NAME).getValue().toString().trim();
  const email     = sheet.getRange(row, COL_EMAIL).getValue().toString().trim();
  const alreadySent = sheet.getRange(row, COL_SENT).getValue();

  // Wysyłaj tylko jeśli email jest uzupełniony i mail nie był jeszcze wysłany
  if (!email || alreadySent) return;

  const payload = JSON.stringify({ name: name, email: email, row: row });

  try {
    const response = UrlFetchApp.fetch(WEBHOOK_URL, {
      method: "post",
      contentType: "application/json",
      headers: { "X-Secret": WEBHOOK_SECRET },
      payload: payload,
      muteHttpExceptions: true,
    });
    Logger.log("Webhook: " + response.getResponseCode() + " " + response.getContentText());
  } catch (err) {
    Logger.log("Błąd webhooka: " + err);
  }
}

// ── Ręczny trigger (opcjonalnie, dla testu) ───────────────────────────────────
// Wejdź w Apps Script → Uruchom → testWebhook
function testWebhook() {
  const payload = JSON.stringify({ name: "Testowy Lead", email: "test@example.com", row: 2 });
  const response = UrlFetchApp.fetch(WEBHOOK_URL, {
    method: "post",
    contentType: "application/json",
    headers: { "X-Secret": WEBHOOK_SECRET },
    payload: payload,
    muteHttpExceptions: true,
  });
  Logger.log(response.getResponseCode() + ": " + response.getContentText());
}
