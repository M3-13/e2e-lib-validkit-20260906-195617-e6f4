# validkit

Eine eigenständige, rein auf der Python-Standardbibliothek basierende Bibliothek mit neun kleinen, voneinander unabhängigen, reinen und typannotierten Prüf- und Normalisierungsfunktionen. Jede Funktion ist einzeln nutzbar, meldet ungültige Eingaben mit einem aussagekräftigen Fehler und besitzt eigene pytest-Unit-Tests inklusive Grenz- und Fehlerfällen.

## Tech-Stack

- **Sprache**: Python (>= 3.9)
- **Tests**: pytest
- **Paketierung**: pyproject.toml (setuptools)
- **Abhängigkeiten**: nur Standardbibliothek (keine externen Pakete)

## Installation

```bash
pip install -e .
```

## Verwendung

Nach der Installation stehen die neun Funktionen direkt unter dem Paketnamen `validkit` zur Verfügung:

```python
from validkit import (
    is_valid_email,
    luhn_check,
    is_valid_iban,
    is_valid_isbn13,
    normalize_phone,
    strip_accents,
    mask_secret,
    slugify,
    clamp,
)
```

Für jede Funktion genau ein lauffähiges Beispiel mit erwarteter Ausgabe:

### is_valid_email

```python
is_valid_email("test@example.com")  # -> True
```

### luhn_check

```python
luhn_check("79927398713")  # -> True
```

### is_valid_iban

```python
is_valid_iban("DE89370400440532013000")  # -> True
```

### is_valid_isbn13

```python
is_valid_isbn13("978-3-16-148410-0")  # -> True
```

### normalize_phone

```python
normalize_phone("030 1234567", "DE")  # -> '+49301234567'
```

### strip_accents

```python
strip_accents("Müller café")  # -> 'Muller cafe'
```

### mask_secret

```python
mask_secret("geheimnisvoll", 4)  # -> '**********voll'
```

### slugify

```python
slugify("Héllo, Wörld!")  # -> 'hello-world'
```

### clamp

```python
clamp(5, 0, 10)  # -> 5
```

## Tests

```bash
pytest
```
