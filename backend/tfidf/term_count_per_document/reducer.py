#!/usr/bin/env python3
"""
term_count_per_document/mapper.py

Calculates the total terms in each document.

Input: (docid, term, term_count)
Output: (docid+term, term_count, term_count_per_docid)
"""

import sys

current_key = None      # Tracks the full key (term + docid)
current_docid = None    # Tracks the current docid
current_count = 0       # Tracks total terms within the current docid

for line in sys.stdin:
    line = line.strip()
    docid, term, term_count = line.split('\t', 2)  # Two tabs expected

    try:
        term_count = int(term_count)
    except ValueError:
        continue  # Ignore/discard invalid lines

    key = f"{term}+{docid}"  # Track by unique key

    # Print when the key changes
    if current_key and current_key != key:
        print(f"{current_key}\t{term_count}\t{current_count}")

    # Reset count only when the docid changes
    if current_docid != docid:
        current_count = 0  # Reset total term count for new docid

    # Accumulate counts
    current_count += term_count
    current_key = key
    current_docid = docid

# Output the last key if needed
if current_key:
    print(f"{current_key}\t{term_count}\t{current_count}")
