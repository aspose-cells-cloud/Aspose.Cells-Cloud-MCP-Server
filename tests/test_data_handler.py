"""Load sample workbook content as Base64 text for the integration tests.

Fixtures live in ``tests/fixtures/`` and are generated offline by
``tests/generate_fixtures.py`` (stdlib only, no cloud or third-party libs).
Override the directory with the ``ASPOSE_TEST_DATA_DIR`` env var if you keep
your own sample files elsewhere.

The loader intentionally returns an empty string when a fixture is missing so a
misconfigured environment degrades to the existing graceful path instead of a
hardcoded developer-machine path.
"""

import base64
import os
from pathlib import Path

_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def _load(name: str) -> str:
    fixture_dir = Path(os.getenv("ASPOSE_TEST_DATA_DIR", _FIXTURES_DIR))
    path = fixture_dir / name
    if not path.is_file():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def get_book1_xlsx() -> str:
    return _load("Book1.xlsx")


def get_booktext_xlsx() -> str:
    return _load("BookText.xlsx")


def get_book_text_ods() -> str:
    return _load("BookText.ods")
