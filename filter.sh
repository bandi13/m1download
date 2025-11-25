#!/usr/bin/env bash
# ------------------------------------------------------------
# filter-dividends.sh
#   Keep only rows whose "Transaction Type" column equals DIVIDEND
#
# Usage:
#   ./filter-dividends.sh  INPUT.csv  [OUTPUT.csv]
#
#   INPUT.csv   – path to the source CSV (required)
#   OUTPUT.csv  – optional path for the filtered CSV.
#                 If omitted the result is printed to STDOUT.
#
# Dependencies:
#   * awk (POSIX‑compatible, comes with every Linux/macOS)
#   * grep, cut – also standard utilities
# ------------------------------------------------------------

set -euo pipefail   # safety: fail on errors, undefined vars, pipe failures

# ---------- 1. Parse arguments ----------
if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 INPUT.csv [OUTPUT.csv]" >&2
    exit 1
fi

INPUT=$1
OUTPUT=${2:-/dev/stdout}   # empty string means “write to stdout”

# ---------- 2. Find the column number of “Transaction Type” ----------
# The header line is the first line of the file.
# We split it on commas that are **not** inside double quotes.
# The trick with awk's FPAT makes it CSV‑aware without external libs.

# FPAT = “field pattern” – a regex that describes a *field*.
# The pattern below matches either:
#   • a quoted string (including commas inside it)   OR
#   • a sequence of non‑comma characters.
awk '
BEGIN {
    # CSV‑aware field splitter:
    FPAT = "([^,]*|\"[^\"]*\")+"
}
NR == 1 {
    for (i = 1; i <= NF; i++) {
        # Remove surrounding quotes for the comparison
        gsub(/^"|"$/, "", $i)
        if ($i == "Transaction Type") {
            col = i
            break
        }
    }
    if (!col) {
        printf "ERROR: Could not find a column named \"Transaction Type\" in %s\n", FILENAME > "/dev/stderr"
        exit 1
    }
    # Print the header line unchanged (so the output is still a CSV)
    print
    next
}
col && $col == "DIVIDEND" {
    print
}
' "$INPUT" | \
    awk '
BEGIN {
    # CSV‑aware field splitter:
    #   - a quoted string (including commas inside) OR
    #   - a sequence of characters that are not commas.
    FPAT = "([^,]*|\"[^\"]*\")+"
}
NR == 1 {
    # Find the column numbers for the three headers we care about.
    for (i = 1; i <= NF; i++) {
        # Strip surrounding double quotes for comparison
        gsub(/^"|"$/, "", $i)

        if ($i == "Posted Date")   posted = i
        else if ($i == "Symbol")   symbol = i
        else if ($i == "Amount")   amount = i
    }

    # Verify that we found all three columns.
    if (!posted || !symbol || !amount) {
        printf "ERROR: Could not locate one or more required columns (Posted Date, Symbol, Amount) in %s\n",
               FILENAME > "/dev/stderr"
        exit 1
    }

    # Print a header line that contains only the three columns (in the requested order)
    printf "%s,%s,%s\n", $posted, $symbol, $amount
    next
}
{
    # Print the three fields for every data row.
    printf "%s,%s,%s\n", $posted, $symbol, $amount
}
' | tac   > "${OUTPUT}"
