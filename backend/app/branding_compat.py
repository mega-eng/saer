"""توافق جلسات وملفات الإصدارات السابقة دون تعديل محتواها."""
from pathlib import Path
from typing import Mapping

SESSION_COOKIE = "saer_session"
LEGACY_SESSION_COOKIE = "siarad_session"

def session_token(cookies: Mapping[str, str]) -> str | None:
    return cookies.get(SESSION_COOKIE) or cookies.get(LEGACY_SESSION_COOKIE)

def database_path(directory: Path) -> Path:
    current = directory / "saer.sqlite"
    legacy = directory / "siarad.sqlite"
    return legacy if not current.exists() and legacy.exists() else current
