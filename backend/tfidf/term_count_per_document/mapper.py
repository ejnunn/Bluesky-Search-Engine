#!/usr/bin/env python3
"""
term_count_per_document/mapper.py

Calculates the total terms in each document.

Input: (term+docid, term_count)
Output: (docid, term, term_count)
"""

import sys

for line in sys.stdin:
    line = line.strip()
    # (docid+term, term_count)
    term_docid, term_count = line.split('\t')
    term, docid = term_docid.split('+')

    print(f"{docid}\t{term}\t{term_count}")