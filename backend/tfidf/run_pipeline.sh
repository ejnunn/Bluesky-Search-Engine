#!/bin/bash
# TF-IDF Pipeline for Bluesky Data

DB_NAME=../../bluesky_posts.db
DB_PATH="../../bluesky_posts.db"
OUTPUT_DIR="output"

# Ensure output directory exists
mkdir -p $OUTPUT_DIR

echo "Calculating TF-IDF from database: $DB_PATH"

# Step 1: Extract posts from the database and clean newlines within posts
echo "Fetching posts from database..."
sqlite3 $DB_NAME "SELECT author_handle, REPLACE(REPLACE(content, CHAR(13), ''), CHAR(10), ' ') AS content FROM posts;" > output/posts.txt


# Step 2: Run the Term Count Job
echo "Running Term Count Job: (author_handle | content) -> (term+author_handle, term_count)"
cat $OUTPUT_DIR/posts.txt | python3 term_count/mapper.py | sort | python3 term_count/reducer.py > $OUTPUT_DIR/term_counts.txt

# Step 3: Run the Term Count per Document Job
echo "Running Term Count per Document Job: (term+author_handle, term_count) -> (term+author_handle, term_count, terms_per_doc)"
cat $OUTPUT_DIR/term_counts.txt | python3 term_count_per_document/mapper.py | sort | python3 term_count_per_document/reducer.py > $OUTPUT_DIR/term_count_per_document.txt

# Step 4: Run the TF-IDF Job
echo "Running TF-IDF Job: (term+author_handle, term_count, terms_per_doc) -> (term, author_handle, tf_idf)"
cat $OUTPUT_DIR/term_count_per_document.txt | python3 tfidf/mapper.py | sort | python3 tfidf/reducer.py > $OUTPUT_DIR/tfidf.txt

# Step 5: Insert TF-IDF results into the database
echo "Inserting TF-IDF scores back into database..."
sqlite3 $DB_PATH <<EOF
DROP TABLE IF EXISTS tfidf;
CREATE TABLE tfidf (
    term TEXT,
    author_handle TEXT,
    score REAL
);

.separator "\t"
.import $OUTPUT_DIR/tfidf.txt tfidf
EOF

echo "TF-IDF calculation complete."
