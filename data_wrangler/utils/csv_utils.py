import csv

class CSVUtils:
    """
    Utility class for reading and writing CSV files.
    """

    @staticmethod
    def read_csv(file_path):
        """
        Read a CSV file and return its contents as a list of dictionaries and the fieldnames.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            tuple: Contents of the CSV file and the fieldnames.
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            data = [row for row in reader]
            fieldnames = reader.fieldnames
            return data, fieldnames

    @staticmethod
    def write_csv(file_path, data, fieldnames=None):
        """
        Write a list of dictionaries to a CSV file, preserving column order if fieldnames are provided.

        Args:
            file_path (str): Path to the output CSV file.
            data (list of dict): Data to write to the file.
            fieldnames (list of str, optional): List of fieldnames to preserve column order.
        """
        if not data:
            return
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)