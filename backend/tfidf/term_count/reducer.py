#!/usr/bin/env python3
"""
term_count/reducer.py

Term count refers to the count of each term in each document.
Identical terms from different documents represent separate term counts in this context.
"""

import sys

current_word = None
current_count = 0

for line in sys.stdin:
    # Remove leading and trailing whitespace
    line = line.strip()

    # Parse the input from mapper
    try:
        word, count = line.split("\t", 1)
        count = int(count)  # Convert count from string to int
    except ValueError:
        continue  # Ignore malformed lines

    # Since Hadoop sorts input by key before sending to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # Output the final count for the previous word
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

# Ensure the last word is outputted
if current_word:
    print(f"{current_word}\t{current_count}")
