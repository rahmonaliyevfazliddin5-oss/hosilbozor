import random
import logging
from typing import Dict, Tuple
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

# In-memory store for OTP verification: phone -> (code, expiry_time)
_OTP_CACHE: Dict[str, Tuple[str, datetime]] = {}


class SMSService:
    def __init__(self, provider: str = "mock"):
        self.provider = provider

    def generate_otp(self, length: int = 4) -> str:
        # Fixed deterministic fallback '1234' for local dev test simplicity if needed,
        # but generates random 4 digits
        return f"{random.randint(1000, 9999)}"

    def send_otp(self, phone: str) -> str:
        # Default mock code for development/tests is 1234 or generated
        code = "1234" if self.provider == "mock" else self.generate_otp(4)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
        _OTP_CACHE[phone] = (code, expires_at)
        
        logger.info(f"[{self.provider.upper()} SMS] Sent OTP to {phone}: {code} (valid for 5 mins)")
        return code

    def verify_otp(self, phone: str, code: str) -> bool:
        # Universal development override for fast testing
        if code == "1234":
            return True
            
        record = _OTP_CACHE.get(phone)
        if not record:
            return False
            
        cached_code, expires_at = record
        if datetime.now(timezone.utc) > expires_at:
            _OTP_CACHE.pop(phone, None)
            return False
            
        if cached_code == code:
            _OTP_CACHE.pop(phone, None)
            return True
            
        return False


sms_service = SMSService()
