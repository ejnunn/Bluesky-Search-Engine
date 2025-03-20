#!/usr/bin/env python3
"""
tfidf/reducer.py

Input: (term, docid, term_count, term_count_per_docid)
Output: (term+docid, tf_idf)
"""

import sys
import math

# Document frequency dictionary (to track how many docs contain each term)
df_t = {}  # { term: document_count }
doc_counts = []  # Stores each line to process later
docid_set = set()  # Tracks unique document IDs for N

# First pass — collect document frequency and track total documents (N)
for line in sys.stdin:
    line = line.strip()
    try:
        term, docid, term_count, term_count_per_docid = line.split('\t')
        term_count = int(term_count)
        term_count_per_docid = int(term_count_per_docid)
    except ValueError:
        continue  # Ignore malformed lines

    doc_counts.append((term, docid, term_count, term_count_per_docid))

    # Track unique doc IDs for total document count
    docid_set.add(docid)

    # Track document frequency
    if term not in df_t:
        df_t[term] = set()
    df_t[term].add(docid)

# Total number of documents
N = len(docid_set)

# Second pass — Calculate TF-IDF for each term in each document
for term, docid, term_count, term_count_per_docid in doc_counts:
    tf = term_count / term_count_per_docid
    df = len(df_t[term])
    idf = math.log(N / df) if df > 0 else 0  # Avoid division by zero
    tfidf = tf * idf

    print(f"({term}, {docid})\t{tfidf:.6f}")
