import sqlite3
import re
import nltk
from nltk.corpus import stopwords
from flask import Flask, request, jsonify
from flask_cors import CORS

# Download stopwords if not already present
nltk.download("stopwords")

app = Flask(__name__)
CORS(app) # Allows frontend to make requests

DB_PATH = "bluesky_posts.db"

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text) # Remove punctuation
    words = text.split()
    words = [word for word in words if word not in stopwords.words("english")] # Remove stopwords
    return " ".join(words)

# Query TF-IDF table and get top 5 matches
def search_tfidf(query):
    query = clean_text(query) # Sanitize query before accessing DB
    
    if not query.strip():  # Ensure query is not empty after cleaning
        return []

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    sql_query = """
        SELECT term, author_handle, score FROM tfidf
        WHERE term LIKE ?
        ORDER BY score DESC
        LIMIT 5
    """

    cursor.execute(sql_query, (f"%{query}%",))
    results = cursor.fetchall()
    connection.close()

    return [{"term": row[0], "author_handle": row[1], "score": row[2]} for row in results]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get("q", "")

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = search_tfidf(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
