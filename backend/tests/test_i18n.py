from app.core.i18n import get_translation


def test_i18n_uz_latn():
    text = get_translation("auth.otp_sent", "uz_latn")
    assert "Tasdiqlash kodi" in text


def test_i18n_uz_cyrl():
    text = get_translation("auth.otp_sent", "uz_cyrl")
    assert "Тасдиқлаш коди" in text


def test_i18n_ru():
    text = get_translation("auth.otp_sent", "ru")
    assert "Код подтверждения" in text


def test_i18n_fallback():
    # Unsupported language falls back to uz_latn
    text = get_translation("auth.otp_sent", "unknown_lang")
    assert "Tasdiqlash kodi" in text

    # Missing key falls back to key itself
    text = get_translation("non.existent.key", "uz_latn")
    assert text == "non.existent.key"
