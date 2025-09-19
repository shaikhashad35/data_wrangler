from datetime import datetime
from dateutil import parser
from data_wrangler.core.exceptions import NormalizationError
from data_wrangler.core.strategies.base import ColumnNormalizer

class DateNormalizer(ColumnNormalizer):
    """
    Normalizes dates to ISO 8601 format (YYYY-MM-DD), with support for dynamic configurations.
    """

    def __init__(self, default_format="%d/%m/%Y", pivot_year=25):
        """
        Initialize the DateNormalizer with default configurations.

        Args:
            default_format (str): The default date format to use for parsing.
            pivot_year (int): The pivot year for two-digit year handling.
        """
        self.default_format = default_format
        self.pivot_year = pivot_year

    def normalize(self, dob):
        """
        Normalize a date of birth to ISO 8601 format, following specific rules:
        - For ambiguous all-numeric dates (e.g., 01/02/1990), assume day-first (DD/MM/YYYY) unless the month > 12 implies MM/DD/YYYY.
        - Two-digit years: use a pivot of 25 → years 00–25 → 2000–2025; otherwise map to 1900–1999.

        Args:
            dob (str): The date of birth to normalize.

        Returns:
            str: Normalized date of birth.

        Raises:
            NormalizationError: If the date is invalid, with a reason.
        """
        import re
        if not dob:
            raise NormalizationError("Date of birth is missing.")
        dob = dob.strip()
        # Acceptable delimiters
        delimiters = ['/', '-', '.', '_']
        for delim in delimiters:
            dob = dob.replace(delim, '/')
        dob = re.sub(r'\s+', ' ', dob)
        dob = dob.strip()
        # Try custom rules for ambiguous numeric dates and two-digit years
        match = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{2,4})$', dob)
        if match:
            first, second, year = int(match.group(1)), int(match.group(2)), match.group(3)
            if len(year) == 2:
                year = int(year)
                if year <= self.pivot_year:
                    year += 2000
                else:
                    year += 1900
            else:
                year = int(year)
            # If month > 12, treat as MM/DD/YYYY
            if second > 12:
                month, day = first, second
            else:
                day, month = first, second
            try:
                dt = datetime(year, month, day)
                return dt.strftime("%Y-%m-%d")
            except Exception:
                raise NormalizationError(f"Invalid date: {dob} (day={day}, month={month}, year={year})")
        # Fallback to dateutil.parser for all other formats
        try:
            dt = parser.parse(dob, dayfirst=True, yearfirst=False, fuzzy=True)
            # Handle two-digit years with pivot
            if dt.year < 100:
                if dt.year <= self.pivot_year:
                    dt = dt.replace(year=2000 + dt.year)
                else:
                    dt = dt.replace(year=1900 + dt.year)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            raise NormalizationError(f"Invalid date format: {dob}. Supported: ISO, numeric, month name formats, and natural language dates.")