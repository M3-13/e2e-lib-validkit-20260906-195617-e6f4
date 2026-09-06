VERDICT: CHANGES_REQUESTED

## Sicherheitsbericht

### 1. Secrets

Keine hartkodierten Schlüssel, Passwörter, Token oder verdächtigen URLs gefunden. Die Fehlermeldungen der Funktionen geben in den regulären Pfaden keine Eingabewerte aus; die Tests bestätigen dies für die üblichen Fälle.

### 2. Injection & Eingaben

Das Projekt ist eine reine Bibliothek ohne Datei-, Netzwerk- oder Datenbankzugriffe. Klassische Injection-Risiken wie SQL, Command, Path oder SSRF entfallen damit.

**Mittel – `validkit/luhn.py` – AC-13-Verletzung bei Unicode-Ziffern**

`luhn_check` validiert Zeichenketten mit `str.isdigit()`. Diese Methode liefert auch für Zeichen wie `"²"` (hochgestellte Ziffer) `True`, obwohl `int()` solche Zeichen nicht parsen kann. Dadurch kann eine unkontrollierte `ValueError`-Meldung entstehen, z. B.:

```
invalid literal for int() with base 10: '²'
```

Diese Meldung enthält einen Teil der übergebenen Eingabe und verletzt damit die Sicherheitsanforderung AC-13, wonach keine öffentliche Funktion Eingabewerte in Exception-Messages ausgeben darf.

**Konkreter Fix:**

```python
if isinstance(digits, str):
    if not digits:
        raise ValueError("digits must not be empty")
    if not digits.isascii() or not digits.isdigit():
        raise ValueError("digits must contain only digit characters")
```

Alternativ:

```python
if any(ch < "0" or ch > "9" for ch in digits):
    raise ValueError("digits must contain only digit characters")
```

Zusätzlich sollte ein Test ergänzt werden, der z. B. `luhn_check("²²")` auf `ValueError` prüft und sicherstellt, dass die Fehlermeldung kein Eingabezeichen enthält.

**Niedrig – `validkit/email.py` – sehr permissive E-Mail-Validierung**

Der reguläre Ausdruck `r"[^@\s]+@[^@\s]+\.[^@\s]+"` erfüllt zwar die ReDoS-Anforderung AC-14 und ist linear, akzeptiert aber ungewöhnliche lokale Teile wie `"a..b@example.com"`, `".a@example.com"` oder `"a(b)c@example.com"`. Das ist keine unmittelbar ausnutzbare Schwachstelle, kann aber problematisch sein, wenn die Funktion als letzte Validierung vor sicherheitskritischen Aktionen wie Passwort-Reset oder Einladungen verwendet wird.

**Konkreter Fix (optional):**

```python
_EMAIL_RE = re.compile(
    r"[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?"
    r"(?:\.[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?)+",
    re.IGNORECASE,
)
```

Dabei muss die bestehende Vertragserfüllung erhalten bleiben: `"test@example.com"` bleibt gültig, `"test@example"` bleibt ungültig.

**Niedrig – `validkit/phone.py` – ungeprüfte numerische Ländercodes**

`_resolve_dial_code` akzeptiert jede rein numerische Zeichenfolge als Ländercode, z. B. `"000"` oder beliebig lange Ziffernfolgen. Das ist kein direkter Injection-Vektor, kann aber unerwartete E.164-Ausgaben erzeugen.

**Konkreter Fix (optional):**

Die numerische Eingabe gegen die bekannten Dial-Codes prüfen oder auf eine sinnvolle Länge begrenzen:

```python
if candidate.isdigit():
    if candidate not in _DIAL_CODE_BY_COUNTRY.values():
        raise ValueError("unknown country code")
    return candidate
```

### 3. AuthN/AuthZ

Nicht anwendbar. Die Bibliothek enthält keine Benutzer-, Sitzungs- oder Zugriffslogik.

### 4. Abhängigkeiten

Das Projekt verwendet ausschließlich die Python-Standardbibliothek. Es sind keine Drittanbieter-Abhängigkeiten und damit keine bekannten verwundbaren Pakete vorhanden. Die Scanner `bandit` und `semgrep` wurden als `[skipped]` gemeldet und konnten nicht ausgeführt werden; das ist eine Prüflücke, aber aus der Lücke selbst wird kein Befund abgeleitet.

### 5. Konfiguration & Transport

Nicht anwendbar. Es gibt keine Server-, Netzwerk- oder Debug-Konfiguration. Die Build-Konfiguration in `pyproject.toml` enthält keine unsicheren Vorgaben.

## Fazit

Keine kritischen oder hohen Schwachstellen. Es besteht jedoch eine konkrete, wenn auch eng begrenzte AC-13-Verletzung in `luhn_check`, die vor dem Ship behoben werden sollte. Daher: **CHANGES_REQUESTED**.