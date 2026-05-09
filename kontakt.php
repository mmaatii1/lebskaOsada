<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: https://kaszubskaosada.com.pl');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method not allowed']);
    exit;
}

$raw = file_get_contents('php://input');
$data = json_decode($raw, true);

if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Invalid JSON']);
    exit;
}

function clean(mixed $v): string {
    return htmlspecialchars(trim((string)($v ?? '')), ENT_QUOTES, 'UTF-8');
}

$type = clean($data['type'] ?? 'contact'); // 'contact' | 'callback'

if ($type === 'callback') {
    $name  = clean($data['name'] ?? '');
    $phone = clean($data['phone'] ?? '');

    if ($name === '' || $phone === '') {
        http_response_code(422);
        echo json_encode(['ok' => false, 'error' => 'Brakuje imienia lub telefonu']);
        exit;
    }

    $subject = "Prośba o oddzwonienie – {$name}";
    $body = <<<TEXT
        Nowe zgłoszenie z formularza popup (oddzwonienie):

        Imię:    {$name}
        Telefon: {$phone}
        TEXT;
} else {
    $name    = clean($data['name'] ?? '');
    $phone   = clean($data['phone'] ?? '');
    $email   = filter_var(trim((string)($data['email'] ?? '')), FILTER_VALIDATE_EMAIL);
    $message = clean($data['message'] ?? '');

    if ($name === '' || $email === false) {
        http_response_code(422);
        echo json_encode(['ok' => false, 'error' => 'Brakuje imienia lub poprawnego e-maila']);
        exit;
    }

    $subject = "Zapytanie z landing page – {$name}";
    $body = <<<TEXT
        Nowe zapytanie z formularza kontaktowego:

        Imię i nazwisko: {$name}
        Telefon:         {$phone}
        E-mail:          {$email}
        Wiadomość:
        {$message}
        TEXT;
}

$recipients = ['jaroslaw.szreder@lebskaosada.pl', 'mmaatii122@gmail.com', 'sprzedaz@lebskaosada.pl'];
$headers = implode("\r\n", [
    'From: Lebska Osada <noreply@lebskaosada.pl>',
    'Reply-To: ' . ($email ?? $recipients[0]),
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . PHP_VERSION,
]);

$sent = true;
foreach ($recipients as $to) {
    if (!mail($to, $subject, $body, $headers)) {
        $sent = false;
    }
}

if (!$sent) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Błąd serwera – spróbuj ponownie']);
    exit;
}

$ch = curl_init('https://script.google.com/macros/s/AKfycbxfkvETeuarmUdlJ6JpUi2NdA9JZi15RDCcLnPOnUH4VkahUYePhIfb0tTbVKn44ck_lw/exec');                                            
  curl_setopt_array($ch, [                                                                                                                                                        
      CURLOPT_POST           => true,                                                                                                                                             
      CURLOPT_POSTFIELDS     => json_encode([
          'id'                => uniqid('web_', true),
          'created_time'      => date('Y-m-d H:i:s'),
          'form_name'         => $type,
          'is_organic'        => true,
          'platform'          => 'website',
          'cel_zakupu'        => '',
          'kiedy_kontakt'     => '',
          'termin_prezentacji'=> '',
          'full_name'         => $name,
          'phone_number'      => $phone,
          'email'             => ($email !== false) ? $email : '',
      ]),                                                                                                                                                                         
      CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_TIMEOUT        => 5,                                                                                                                                                
      CURLOPT_FOLLOWLOCATION => true,
  ]);                                                                                                                                                                             
  curl_exec($ch);                                                 
  curl_close($ch);

echo json_encode(['ok' => true]);
