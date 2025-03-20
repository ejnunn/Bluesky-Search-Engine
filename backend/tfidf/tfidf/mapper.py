#!/usr/bin/env python3
"""
tfidf/mapper.py

Input: (term+docid, term_count, term_count_per_docid)
Output: (term, docid, term_count, term_count_per_docid)
"""

import sys

for line in sys.stdin:
	line = line.strip()

	term_docid, term_count, term_count_per_docid = line.split('\t')
	term, docid = term_docid.split('+')
	

	print(f"{term}\t{docid}\t{term_count}\t{term_count_per_docid}")