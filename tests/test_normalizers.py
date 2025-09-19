import pytest
from data_wrangler.core.strategies.date_strategies import DateNormalizer
from data_wrangler.core.strategies.phone_strategies import E164PhoneNormalizer
from data_wrangler.core.exceptions import NormalizationError

class TestDateNormalizer:
    @pytest.fixture(scope="class")
    def normalizer(self):
        return DateNormalizer()

    @pytest.mark.parametrize("input_date,expected", [
        ("2001-09-09", "2001-09-09"),  # Already ISO format
        ("09/01/2001", "2001-01-09"),  # Ambiguous numeric, day-first (DD/MM/YYYY)
        ("13/02/2001", "2001-02-13"),  # Month > 12, so MM/DD/YYYY
        ("09/09/01", "2001-09-09"),    # Two-digit year, pivot < 25, so 2001
        ("09/09/90", "1990-09-09"),    # Two-digit year, pivot > 25, so 1990
        ("Apr-05-2004", "2004-04-05"), # Month name short, parsed as 5 April 2004
        ("April 5, 2004", "2004-04-05"), # Month name long, parsed as 5 April 2004
        ("09.09.2001", "2001-09-09"),  # Different delimiter, parsed as DD.MM.YYYY
        ("09_09_2001", "2001-09-09"),  # Different delimiter, parsed as DD_MM_YYYY
        ("5th April 2004", "2004-04-05"), # Natural language, parsed as 5 April 2004
        ("  09 / 09 / 2001  ", "2001-09-09"), # Whitespace and fuzzy, parsed as DD/MM/YYYY
    ])
    def test_valid_dates(self, normalizer, input_date, expected):
        assert normalizer.normalize(input_date) == expected

    @pytest.mark.parametrize("input_date", [
        "31/02/2001",  # Invalid date (Feb 31 does not exist)
        "",             # Empty string
        "not a date",   # Nonsense string
    ])
    def test_invalid_dates(self, normalizer, input_date):
        with pytest.raises(NormalizationError):
            normalizer.normalize(input_date)

class TestE164PhoneNormalizer:
    @pytest.fixture(scope="class")
    def normalizer(self):
        return E164PhoneNormalizer()

    @pytest.mark.parametrize("input_phone,expected", [
        ("0585108603", "+971585108603"),      # Local UAE style (starts with 0, no country code)
        ("o522458591", "+971522458591"),      # Local UAE style with typo (o→0)
        ("971563341057", "+971563341057"),    # Already has UAE country code (no +)
        ("+91-98765-43210", "+919876543210"), # Already international (+91)
        ("00971585108603", "+971585108603"),  # International with 00
        ("+1-415-555-2671", "+14155552671"),  # Already international (+1)
        ("4402079460958", "+4402079460958"),  # Other country code (known)
        ("  058-510-8603  ", "+971585108603"),# Whitespace and symbols, local UAE style
    ])
    def test_valid_phones(self, normalizer, input_phone, expected):
        assert normalizer.normalize(input_phone) == expected

    @pytest.mark.parametrize("input_phone", [
        "054123",  # Too short (invalid length)
        "058123456789012345",  # Too long (invalid length)
        "563341057",  # Not local, no country code
        "",  # Empty
    ])
    def test_invalid_phones(self, normalizer, input_phone):
        with pytest.raises(NormalizationError):
            normalizer.normalize(input_phone)

class TestStrategyExtensibility:
    def test_strategy_extensibility(self):
        class DummyPhoneNormalizer:
            def normalize(self, raw):
                return "DUMMY"
        normalizer = DummyPhoneNormalizer()
        assert normalizer.normalize("any") == "DUMMY"
