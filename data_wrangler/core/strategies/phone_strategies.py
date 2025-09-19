from data_wrangler.core.constants import DEFAULT_COUNTRY_CODE
from typing import Optional
import re
from data_wrangler.core.exceptions import NormalizationError
from data_wrangler.core.strategies.base import ColumnNormalizer

class E164PhoneNormalizer(ColumnNormalizer):
    """
    Normalizes phone numbers into E.164 format.
    - Only assumes UAE (+971) if the number starts with 0 and does not already have a country code.
    - If the number already has a country code (starts with +, 00, or a known code like 971, 91, etc.), do not change it—just normalize its format.
    - If the number is local UAE style (starts with 0), drop the 0 and prefix with +971.
    - Gives a clear reason if normalization is not possible.
    """
    def __init__(self, country_code=DEFAULT_COUNTRY_CODE):
        self.country_code = country_code
        self.char_replacements = {'O': '0', 'o': '0'}
        self.known_codes = ["971", "91", "1", "44", "380", "49", "81", "7"]

    def clean_raw(self, raw: str) -> str:
        if not raw:
            return ""
        for bad, good in self.char_replacements.items():
            raw = raw.replace(bad, good)
        cleaned = re.sub(r"[^\d+]+", "", raw)
        if cleaned.count("+") > 1:
            cleaned = "+" + cleaned.replace("+", "")
        return cleaned

    def has_country_code(self, phone: str) -> bool:
        if phone.startswith("+") or phone.startswith("00"):
            return True
        for code in self.known_codes:
            if phone.startswith(code):
                return True
        return False

    def normalize(self, raw: str) -> str:
        """
        Normalize the phone number to E.164 format or raise NormalizationError with a reason.
        """
        if not raw:
            raise NormalizationError("Phone number is missing.")
        phone = self.clean_raw(raw)
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) < 8 or len(digits_only) > 15:
            raise NormalizationError(f"Phone number length invalid: {len(digits_only)} digits (must be 8-15)")
        # Already has country code
        if self.has_country_code(phone):
            if phone.startswith("00"):
                return "+" + phone[2:]
            if phone.startswith("+"):
                return phone
            return "+" + phone
        # Local UAE style (starts with 0, no country code)
        if phone.startswith("0"):
            return self.country_code + phone[1:]
        # If not local and no country code, invalid
        raise NormalizationError(
            "Phone number must include a country code or start with 0 for local UAE numbers.")

