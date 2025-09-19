# Data Wrangler

## Overview
Data Wrangler is a Python tool designed to normalize contact data from CSV files. It processes phone numbers and dates of birth to ensure consistent formatting, following best practices and extensible design.

## Features
- Normalize phone numbers to E.164 format (with UAE default logic for local numbers)
- Normalize dates of birth to ISO 8601 format (YYYY-MM-DD), handling ambiguous and natural language dates
- Extensible strategy pattern for future normalization logic
- Summary reporting of processed, normalized, and skipped rows
- Unit tests for robust validation

## Setup

### 1. Install Docker
- Download Docker Desktop for Mac from: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
- Follow the installation instructions and start Docker Desktop.
- Verify installation:
  ```bash
  docker --version
  ```

### 2. Build the Docker Image
From the project root directory, run:
```bash
docker build -t data-wrangler .
```

### 3. Run the Main Script (Normalize Contacts)
```bash
docker run --rm -v $(pwd):/app data-wrangler
```
- This will process the sample CSV and output a normalized file in the `results/` directory.

### 4. Run Unit Tests
```bash
docker run --rm -v $(pwd):/app -e PYTHONPATH=/app data-wrangler pytest tests/test_normalizers.py
```
- This will execute all unit tests for phone and date normalization logic.

## Local (Non-Docker) Usage
If you prefer to run locally:
1. Install Python 3.9+
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python3 normalize_contacts.py
   ```
4. Run tests:
   ```bash
   pytest tests/test_normalizers.py
   ```

## Input/Output
- **Input:** `tests/sample_data/contacts_sample_open.csv` (semicolon-delimited)
- **Output:** Normalized CSV in `results/` with a timestamped filename

## Approach & Thought Process

### Phone Normalization
- **Goal:** Normalize phone numbers to E.164 format, following international best practices and business rules.
- **Logic:**
  - If the number starts with `0` and has no country code, assume UAE (+971), drop the leading 0, and prefix with +971.
  - If the number already has a country code (starts with `+`, `00`, or a known code like `971`, `91`, etc.), do not change the country code—just normalize its format.
  - Common OCR/typo errors (like `o` for `0`) are handled.
  - Length validation is enforced (8–15 digits for E.164).
  - If the number is invalid (wrong length, missing country code, or not local UAE style), a clear error is raised.
- **Extensibility:**
  - The phone normalization logic is implemented as a strategy class (`E164PhoneNormalizer`).
  - New strategies can be added and registered easily for other countries or formats.

### Date Normalization
- **Goal:** Normalize dates to ISO 8601 format (YYYY-MM-DD), handling a wide variety of real-world formats.
- **Logic:**
  - For ambiguous all-numeric dates (e.g., 01/02/1990), assume day-first (DD/MM/YYYY) unless the month > 12 implies MM/DD/YYYY.
  - Two-digit years use a pivot of 25: years 00–25 → 2000–2025, otherwise 1900–1999.
  - Supports a wide range of delimiters and month name formats (e.g., `Apr-05-2004`, `April 5, 2004`).
  - Uses `dateutil.parser` for robust parsing of natural language and edge cases.
  - Invalid or ambiguous dates raise a clear error with a reason.
- **Extensibility:**
  - The date normalization logic is encapsulated in a strategy class (`DateNormalizer`).
  - Additional strategies or custom rules can be added as needed.

### Testing
- **Unit tests** are provided for both phone and date normalization, covering:
  - Standard, edge, and negative cases (invalid input, ambiguous formats, typos, etc.)
  - Each test case includes a comment explaining the expected output and reasoning.
  - Tests are structured using `pytest` classes and fixtures for clarity and maintainability.
  - Extensibility is demonstrated by testing the ability to swap in new strategies.

### Input & Output
- **Input sample:**
  - The input CSV file is stored at `tests/sample_data/contacts_sample_open.csv`.
  - The file is semicolon-delimited and contains columns such as `id`, `phone`, and `dob`.
- **Output sample:**
  - Normalized output files are stored in the `results/` directory.
  - Each output file is named with a timestamp, e.g., `results/normalized_contacts_20250920_021633.csv`.
  - The output preserves the original column order from the input.

## Extensibility
- Easily add new normalization strategies for any column by implementing a new strategy class and registering it in the normalizer.

## Troubleshooting
- If you see `zsh: command not found: docker`, install Docker as described above.
- If you see `zsh: command not found: pytest`, install pytest with `pip3 install pytest` or use Docker for testing.

