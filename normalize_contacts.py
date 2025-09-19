import csv
from datetime import datetime
import time
from data_wrangler.core.normalizer import Normalizer
from data_wrangler.utils.csv_utils import CSVUtils
from data_wrangler.core.exceptions import NormalizationError

def main():
    """
    Main function to normalize contact data from an input CSV file.
    Reads the input file, processes the data, and writes the normalized output.
    """
    input_file = 'tests/sample_data/contacts_sample_open.csv'

    # Generate a unique output file name with a timestamp
    current_time = time.strftime('%Y%m%d_%H%M%S')
    output_file = f'results/normalized_contacts_{current_time}.csv'

    try:
        # Read input CSV
        data, fieldnames = CSVUtils.read_csv(input_file)

        # Normalize data
        normalizer = Normalizer()
        normalized_data, skipped_rows = normalizer.normalize_data(data)

        # Write output CSV with original fieldnames
        CSVUtils.write_csv(output_file, normalized_data, fieldnames=fieldnames)

        # Print summary
        print(f"Rows processed: {len(data)}")
        print(f"Rows normalized: {len(normalized_data)}")
        print(f"Rows skipped: {len(skipped_rows)}")
        if skipped_rows:
            print("Skipped rows:")
            for row, reason in skipped_rows:
                print(f"Row: {row}, Reason: {reason}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()