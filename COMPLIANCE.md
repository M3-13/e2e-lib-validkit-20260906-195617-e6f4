VERDICT: CHANGES_REQUESTED

## Prüfbericht validkit

### 1. Datenschutz / DSGVO

**Befund 1 — mittel — `validkit/luhn.py`: Eingabedaten können in einer Exception-Message austreten (AC-13 verletzt).**  
Die Funktion nutzt `digits.isdigit()` als Vorfilter. Für bestimmte Unicode-Zeichen wie `²` liefert `str.isdigit()` `True`, obwohl `int(char)` später scheitert. Dann wirft Python eine native `ValueError`, deren Meldung das übergebene Zeichen enthält — z. B. `invalid literal for int() with base 10: '²'`. Da `luhn_check` typischerweise Kreditkartennummern prüft, widerspricht das der Sicherheitsvorgabe AC-13, wonach keine öffentliche Funktion übergebene Eingabewerte in Exception-Messages ausgeben darf.  
**Abhilfe:** In `validkit/luhn.py` die Ziffernprüfung auf ASCII-Ziffern einschränken, etwa:
```python
if not digits.isascii() or not digits.isdigit():
    raise ValueError("digits must contain only digit characters")
```
oder direkt:
```python
if any(ch < "0" or ch > "9" for ch in digits):
    raise ValueError("digits must contain only digit characters")
```
Damit wird die native `int()`-Exception mit Eingabeinhalt vermieden.

**Bewertung übrige DSGVO-Aspekte:**  
Die Bibliothek speichert, protokolliert oder überträgt keine personenbezogenen Daten. Alle Funktionen arbeiten rein im Arbeitsspeicher des Aufrufers und geben entweder boolesche Werte, normalisierten Text oder maskierte Werte zurück. `mask_secret` unterstützt datensparsames Maskieren. Für die Bibliothek selbst ist keine datenschutzrechtliche Rechtsgrundlage erforderlich, da sie keine Verarbeitung beim Anbieter bewirkt. Verantwortlich bleibt der jeweilige Integrator. Insoweit sind keine offenen DSGVO-Blocker erkennbar.

### 2. EU Cyber Resilience Act (CRA)

**Befund 2 — mittel — Sicherheitsdokumentation / SBOM und klare Aktualisierungsangaben fehlen sichtbar.**  
Die Software ist eine Bibliothek ohne Fremdabhängigkeiten (`dependencies = []` in `pyproject.toml`), was das CRA-Risiko erheblich senkt. Es fehlt jedoch sichtbar:
- eine `SECURITY.md` mit Sicherheitseigenschaften, Update-Weg und Meldemöglichkeit,
- eine SBOM- bzw. Dependency-Dokumentation,
- im `[project]`-Block Angaben wie `license`, `authors` und `urls` (Repository, Bugtracker).

**Abhilfe:**  
`pyproject.toml` ergänzen:
```toml
[project]
license = {text = "MIT"}            # passende Lizenz wählen
authors = [{name = "...", email = "..."}]
urls = {repository = "...", issues = "..."}
```
Zusätzlich neu anlegen:
- `SECURITY.md`: „validkit nutzt ausschließlich die Python-Standardbibliothek; Updates erfolgen über `pip install --upgrade validkit`; Sicherheitsmeldungen bitte an …“
- `SBOM.md` oder maschinenlesbare SBOM (z. B. CycloneDX): „Keine Fremdabhängigkeiten; Laufzeitumgebung Python ≥ 3.9; Komponenten: Python-Standardbibliothek.“  
Damit sind die für eine kleine Bibliothek realistischen CRA-Anforderungen nachvollziehbar dokumentiert.

**Befund 3 — niedrig — Widerspruch zwischen Produktdefinition und Implementierung bei `mask_secret`.**  
Die Acceptance Criteria AC-08 verlangen laut Spec für `mask_secret('geheimnisvoll', 4)` die Ausgabe `'**********voll'` (10 Sternchen). Die sichtbare Implementierung und die Tests liefern dagegen `'*********voll'` (9 Sternchen). Der Text `"geheimnisvoll"` hat 13 Zeichen; bei `keep = 4` sind korrekt 9 Sternchen zu erwarten.  
**Abhilfe:** Die Spezifikation in AC-08 auf `'*********voll'` korrigieren, sofern die Implementierung als maßgeblich akzeptiert wird. Weder Code noch Tests ändern, da sie in sich konsistent sind.

### 3. EU AI Act

Nicht anwendbar. Das Produkt enthält keine KI-Funktionen im Sinne des AI Act.

### 4. Pflichttexte & UI

Nicht anwendbar. Es handelt sich um eine reine `python-backend`-Bibliothek ohne Endnutzer-UI; Impressum, Datenschutzerklärung, Cookie-Banner, Widerrufsbelehrung und ähnliche Web-/Shop-Pflichten fallen deshalb nicht an.

### 5. Barrierefreiheit

Nicht anwendbar. Es existiert keine öffentliche Web-UI, daher keine WCAG-/BITV-/EAA-Pflicht.

### 6. Sonstige Produkt-/Sicherheitsbewertung

Die übrigen sicherheitsrelevanten Vorgaben sind im sichtbaren Code erfüllt:
- AC-01: Paket importierbar, keine externen Pakete.
- AC-13: wird bis auf den Luhn-Unicode-Randfall eingehalten; alle übrigen öffentlichen Funktionen werfen typisierte Fehler ohne Eingabewerte.
- AC-14: Der E-Mail-Regex `[^@\s]+@[^@\s]+\.[^@\s]+` enthält keine verschachtelten Quantoren; kein erkennbares ReDoS-Risiko.
- Keine Protokollierung, keine Persistenz, keine Netzwerkzugriffe; `.gitignore` schließt `.env` und Logdateien aus.

## Ergebnis

CHANGES_REQUESTED wegen des konkreten, behebbaren AC-13-Verstoßes in `validkit/luhn.py`. Aus rechtlicher Sicht liegt kein fundamentaler Datenschutzverstoß vor; die Codepunkte für CRA-Dokumentation sind Marktreifeempfehlungen und der AC-08-Widerspruch ist ein niedriges Produktkonformitätsproblem.