import json
from pathlib import Path
from typing import Dict, Any

_LOCALES_DIR = Path(__file__).resolve().parent.parent / "i18n" / "locales"
_TRANSLATIONS: Dict[str, Dict[str, Any]] = {}

DEFAULT_LANGUAGE = "uz_latn"
SUPPORTED_LANGUAGES = ["uz_latn", "uz_cyrl", "ru"]


def _load_translations() -> None:
    global _TRANSLATIONS
    for lang in SUPPORTED_LANGUAGES:
        file_path = _LOCALES_DIR / f"{lang}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                _TRANSLATIONS[lang] = json.load(f)
        else:
            _TRANSLATIONS[lang] = {}


_load_translations()


def get_translation(key_path: str, lang: str = DEFAULT_LANGUAGE) -> str:
    """
    Resolve a dot-notated translation key like 'auth.otp_sent' for a target language,
    falling back to DEFAULT_LANGUAGE (uz_latn) if missing.
    """
    if lang not in _TRANSLATIONS or not _TRANSLATIONS[lang]:
        _load_translations()

    active_lang = lang if lang in _TRANSLATIONS else DEFAULT_LANGUAGE
    
    # Try active language first
    keys = key_path.split(".")
    val: Any = _TRANSLATIONS.get(active_lang, {})
    found = True
    for k in keys:
        if isinstance(val, dict) and k in val:
            val = val[k]
        else:
            found = False
            break
            
    if found and isinstance(val, str):
        return val

    # Fallback to default language
    if active_lang != DEFAULT_LANGUAGE:
        val = _TRANSLATIONS.get(DEFAULT_LANGUAGE, {})
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return key_path
        if isinstance(val, str):
            return val

    return key_path


t = get_translation
