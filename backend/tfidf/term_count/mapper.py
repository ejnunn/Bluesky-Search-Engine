#!/usr/bin/env python3
"""
term_count/mapper.py - Modified for Bluesky Data
"""

import sys
from nltk.stem import WordNetLemmatizer
from utils import stop_words  # Assuming your utils.py handles stop words

lemma = WordNetLemmatizer()

for line in sys.stdin.buffer.read().decode("utf-8", "ignore").splitlines():
    try:
        author_handle, content = line.strip().split("|", 1)  # Updated delimiter
    except ValueError:
        continue  # Ignore malformed lines

    for word in content.strip().split():
        lowered = word.lower()
        term = "".join(filter(str.isalpha, lowered))  # Keep only alphabetic characters
        term_lemma = lemma.lemmatize(term)

        if term_lemma and term_lemma not in stop_words:
            sys.stdout.buffer.write(f"{term_lemma}+{author_handle}\t1\n".encode("utf-8"))
