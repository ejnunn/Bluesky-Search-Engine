# Bluesky-TF-IDF Search Engine Integration Project

## Overview
This project integrates a Bluesky application for viewing posts with a Python-based TF-IDF search engine. The goal is to build a distributed system that:
- Ingests data from Bluesky,
- Processes the data using TF-IDF calculations via MapReduce,
- Indexes the results in a search engine for efficient querying.

## Architecture
The system is composed of several microservices and components:

- **Data Ingestion Service:** Fetches posts from Bluesky and publishes them to a Kafka topic.
- **TF-IDF Processing:** Uses Apache Hadoop and MapReduce to compute TF-IDF scores from the ingested data.
- **Search Engine:** Indexes and stores processed data in Elasticsearch running on an EC2 instance.
- **Batch Jobs:** Managed via AWS Lambda and EventBridge to periodically trigger data processing and search index updates.
- **Frontend:** A React-based web application that interacts with the backend API to display search results.

## Directory Structure
- **/backend:** Contains services for data ingestion, TF-IDF processing, and integration with the search engine.
- **/frontend:** Contains the React application for the user interface.
- **/tests:** Contains unit, integration, and end-to-end tests.
- **/docs:** Contains documentation including the architecture overview and microservices design.

## Future Steps
Further work will focus on:
- Enhancing error handling and retry logic,
- Scaling microservices with real-time data ingestion via Kafka,
- Expanding the testing strategy and CI/CD pipelines,
- Integrating additional cloud-based monitoring and deployment strategies.

## Running the Project

1. **Ensure Kafka is installed locally.**  

2. **Start the Bluesky Post Producer:**  
   This script fetches posts from Bluesky, publishes them to the `bluesky-posts` Kafka topic, and directly tracks new authors to fetch more posts in future iterations.  

```bash
python3 backend/bluesky_post_producer.py
```

3. **Start the Bluesky Post Consumer:**  
   This script consumes messages from the `bluesky-posts` topic, extracts the necessary fields, and inserts the data into the SQLite database.  

```bash
python3 backend/bluesky_post_consumer.py
```

4. **Monitor Kafka Topics (Optional):**  
   To view the state of the Kafka brokers (locally for now), use the following command in a separate terminal:  

```bash
kcat -b <BROKER> -C -t <TOPIC>
```

5. **Verify Database Contents (Optional):**  
   To inspect the contents of the SQLite database, run the following command:  

```bash
sqlite3 bluesky_posts.db "SELECT * FROM posts;"
```

