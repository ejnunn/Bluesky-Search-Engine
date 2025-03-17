# Architecture Overview

## System Architecture Diagram
[Placeholder for architecture diagram]  
*(An initial diagram should be added here to visually represent the flow between the various services.)*

## Microservices Design and Responsibilities

- **Data Ingestion Service:**
  - Connects to the Bluesky API to fetch raw posts.
  - Preprocesses and publishes posts to a Kafka topic for further processing.
  - Persists raw posts in a durable store for auditing and reprocessing.

- **TF-IDF Processor:**
  - Consumes messages from Kafka.
  - Uses a MapReduce-style job (via Apache Hadoop or a custom Python batch process) to tokenize text, compute term frequency (TF), inverse document frequency (IDF), and generate TF-IDF vectors for each post.
  - Normalizes the computed TF-IDF vectors for use in similarity scoring.

- **Custom Search Engine with Inverted Index:**
  - Builds an inverted index from the computed TF-IDF vectors.
  - Stores the index in a database (e.g., PostgreSQL with JSONB or a NoSQL store) where each term maps to posting lists (document IDs and TF-IDF weights).
  - At query time, computes a TF-IDF vector for the user's search query and uses cosine similarity (or a similar metric) to rank and retrieve the most relevant documents.

- **Batch Processing and Orchestration:**
  - AWS Lambda functions, triggered by AWS EventBridge, manage the scheduled execution of data ingestion, TF-IDF processing, and index updates.
  - Ensures the inverted index remains up-to-date with the latest data.

- **Frontend:**
  - A React-based user interface hosted on AWS S3 and distributed via CloudFront.
  - Interacts with a backend API that handles query processing against the custom inverted index.
  - Displays search results based on custom TF-IDF scoring and similarity measures.

This modular microservices architecture ensures scalability, fault tolerance, and flexibility by decoupling data ingestion, custom text processing, and search functionality while maintaining full control over relevance ranking.
