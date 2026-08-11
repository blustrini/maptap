#!/usr/bin/env bash

set -euo pipefail

show_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] <path_to_csv_file>

Parses a semicolon-delimited country code CSV and generates Python Enum 
member definitions using ISO Alpha-3 codes.

The expected CSV are:
- #1: string representation of the country name
- #3: ISO Alpha-3 code

Options:
  -h, --help    Display this help message and exit.

Arguments:
  <path_to_csv_file>    Path to the CSV file (expects 'Country; ISO Alpha-2; ISO Alpha-3; Numeric').

Example:
  $(basename "$0") country_codes.csv > iso3_members.py
EOF
}

# Handle help options
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    show_help
    exit 0
fi

# Verify an argument was provided
if [ "$#" -ne 1 ]; then
    echo "Error: Missing required argument <path_to_csv_file>." >&2
    echo "" >&2
    show_help >&2
    exit 1
fi

INPUT_FILE="$1"

# Verify the file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' does not exist." >&2
    exit 1
fi

# Extract ISO3 and Country Name
awk -F';' 'NR>1 {
    name=$1; iso3=$3;
    gsub(/^[ \t]+|[ \t]+$/, "", name);
    gsub(/^[ \t]+|[ \t]+$/, "", iso3);
    if (iso3 != "") printf "    %s = \"%s\"  # %s\n", iso3, iso3, name
}' "$INPUT_FILE"