from data_wrangler.core.strategies.phone_strategies import E164PhoneNormalizer
from data_wrangler.core.strategies.date_strategies import DateNormalizer
from data_wrangler.core.exceptions import NormalizationError
from data_wrangler.core.constants import DEFAULT_COUNTRY_CODE

class Normalizer:
    """
    Orchestrates the normalization of contact data using a registry of column normalizers.
    """

    def __init__(self):
        self.normalizers = {
            'phone': E164PhoneNormalizer(DEFAULT_COUNTRY_CODE),
            'dob': DateNormalizer()
        }

    def register_normalizer(self, column, normalizer):
        """
        Register a new normalizer for a specific column.

        Args:
            column (str): The column name.
            normalizer (ColumnNormalizer): The normalizer instance.
        """
        self.normalizers[column] = normalizer

    def normalize_data(self, data):
        """
        Normalize the input data dynamically based on registered normalizers.

        Args:
            data (list of dict): Input data as a list of dictionaries.

        Returns:
            tuple: Normalized data and skipped rows with reasons.
        """
        normalized_data = []
        skipped_rows = []

        for row in data:
            errors = {}
            normalized_row = {}
            # Always normalize phone first
            try:
                if 'phone' in self.normalizers and 'phone' in row:
                    normalized_row['phone'] = self.normalizers['phone'].normalize(row['phone'])
                else:
                    normalized_row['phone'] = row.get('phone')
            except NormalizationError as e:
                errors['phone'] = str(e)
            # Then normalize dob
            try:
                if 'dob' in self.normalizers and 'dob' in row:
                    normalized_row['dob'] = self.normalizers['dob'].normalize(row['dob'])
                else:
                    normalized_row['dob'] = row.get('dob')
            except NormalizationError as e:
                errors['dob'] = str(e)
            # Copy other columns as-is
            for column, value in row.items():
                if column not in ['phone', 'dob']:
                    normalized_row[column] = value
            if errors:
                skipped_rows.append((row, errors))
            else:
                normalized_data.append(normalized_row)

        return normalized_data, skipped_rows