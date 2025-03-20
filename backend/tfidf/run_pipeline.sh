# Setup
corpus_directory=data/state_union/
corpus=$(ls $corpus_directory*.txt)  # Expanding the glob pattern
num_files=$(echo $corpus | wc -w)
mkdir -p output # Ensure the output directory exists

echo "Calculating TF-IDF for the corpus: $corpus_directory"
echo "Number of files: $num_files"
echo "Creating output directory."

# Step 1: Run the Term Count Job
echo "Running the Term Count Job -> (term+docid, term_count)"
for file in $corpus; do
    export map_input_file="$file"
    cat "$file" | python3 term_count/mapper.py | sort | python3 term_count/reducer.py
done > output/term_counts.txt

# Step 2: Run the Term Count per Document Job
echo "Running the Term Count per Document Job -> (docid+term, term_count+terms_per_docid)"
cat output/term_counts.txt | python3 term_count_per_document/mapper.py | sort | python3 term_count_per_document/reducer.py > output/term_count_per_document.txt

# Step 3: Run the TF-IDF Job
echo "Running the TF-IDF Job -> (docid+term, tf_idf)"
cat output/term_count_per_document.txt | python3 tfidf/mapper.py | sort | python3 tfidf/reducer.py > output/tfidf.txt