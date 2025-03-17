# Portfolio Project Specification

## Overview
This project combines two existing side projects:  
1. A small Bluesky application to view posts.
2. A Python search engine using TF-IDF.

The goal is to integrate these into a distributed system that automatically pulls data from Bluesky, computes custom TF-IDF vectors, builds an inverted index for fast search, and allows users to query this data via a web frontend. The project will highlight technical depth, system architecture, and automation skills.

## Key Requirements
1. **Batch Processing**: The system will process data in batches every hour or day, prioritizing availability over consistency.
2. **Microservices Architecture**: The system will include microservices, event-driven components, cloud deployment, and DevOps automation.
3. **Public-Facing API**: A simple web frontend and public API will allow users to interact with the custom search engine.

## Architecture Choices
1. **Backend**
   - **Data Ingestion**: A service pulls posts from Bluesky and publishes them to a Kafka topic.
   - **TF-IDF Processing**: A MapReduce-style job (using Apache Hadoop or a custom Python batch process) computes TF-IDF vectors for each post.
   - **Custom Search Engine with Inverted Index**: Instead of relying on Elasticsearch, the system builds an inverted index that maps terms to posting lists (document IDs and precomputed TF-IDF weights). This index will be used at query time to retrieve and rank documents based on cosine similarity between the query vector and document vectors.
   - **Batch Jobs**: AWS Lambda with EventBridge will schedule batch jobs to run every hour or day. Lambda will trigger the entire data processing pipeline—from ingestion and TF-IDF calculation to inverted index construction.

2. **Frontend**
   - **Framework**: React will be used for the frontend due to its fast ramp-up and ability to build interactive UIs.
   - **Hosting**: The frontend will be hosted statically on AWS S3 with CloudFront for fast global distribution.
   - **API Interaction**: The frontend will query the public API (served by the backend) which performs custom TF-IDF based searches against the inverted index.

3. **Kafka**
   - Kafka will handle the real-time streaming of Bluesky posts for ingestion into the system.
   - Kafka topics will be used to manage data flow between services (data ingestion, TF-IDF processing, and inverted index updates).

4. **Custom Search Engine & Data Store**
   - **Inverted Index Storage**: Rather than using a traditional search engine like Elasticsearch, the processed TF-IDF vectors will be stored as an inverted index. This index can be maintained in a relational or NoSQL database (e.g., PostgreSQL with JSONB or a dedicated search library) where each entry maps a term to a posting list containing document IDs and TF-IDF weights.
   - **Relevance Computation**: At query time, the user’s query is tokenized and its TF-IDF vector computed. A cosine similarity calculation between the query vector and the document vectors (retrieved via the inverted index) is then used to rank and return the top matching documents.

5. **Monitoring**
   - AWS CloudWatch will be used to monitor Lambda functions, the custom search engine service, and the overall data pipeline. Metrics such as job execution times, errors, and system health will be tracked.

## Data Handling
1. **Bluesky Data Ingestion**:  
   - A service pulls raw posts from Bluesky and pushes them to a Kafka topic.
   - Raw posts are stored in a persistent data store for audit and reprocessing.
2. **TF-IDF Calculation**:  
   - A MapReduce job processes raw posts to compute TF-IDF vectors for each document.
   - Each document’s TF-IDF vector is normalized and prepared for indexing.
3. **Inverted Index Construction**:  
   - The system builds an inverted index where each term maps to a posting list containing document IDs and their precomputed TF-IDF weights.
   - This index supports efficient query-time retrieval and custom ranking.
4. **Batch Processing**:  
   - Data is processed in scheduled batches via AWS Lambda and EventBridge, ensuring that the inverted index remains up-to-date with the latest posts.

## Error Handling Strategies
1. **Retries**:  
   - AWS Lambda will automatically retry failed batch jobs. Persistent failures will trigger alerts via CloudWatch.
2. **Logging**:  
   - All processing steps—including data ingestion, TF-IDF computation, and inverted index updates—will include detailed logging for traceability and debugging.

## Testing Plan
1. **Unit Testing**:  
   - Individual components (e.g., Bluesky data ingestion, TF-IDF calculation functions, inverted index updates, and query processing) will have comprehensive unit tests.
2. **Integration Testing**:  
   - The complete data pipeline—from ingestion to inverted index update and query handling—will be tested together in a staging environment.
3. **End-to-End Testing**:  
   - The frontend will be tested to ensure that the user interface interacts correctly with the backend API and returns accurate search results.
4. **Performance Testing**:  
   - The system will be stress-tested with a high volume of posts to ensure that the custom search engine and processing pipeline handle load efficiently.

## Deployment
1. **Frontend Deployment**:  
   - The React app will be deployed as static files to AWS S3, and CloudFront will be used for global CDN distribution.
2. **Backend Deployment**:  
   - The backend services—including data ingestion, TF-IDF processing, and the custom search engine with the inverted index—will be deployed using AWS Lambda (for batch processing) and EC2 or container services for stateful components (e.g., the database holding the inverted index and raw posts).

## Documentation
A `README.md` will be included to explain:
1. **Project Overview**:  
   - A high-level description of the system and its components.
2. **Setup Instructions**:  
   - Step-by-step instructions for setting up the development environment and deploying the system.
3. **Architecture Overview**:  
   - A diagram and explanation of how the various services (data ingestion, TF-IDF processing, inverted index search, and frontend interaction) interact.
4. **Running the System**:  
   - Detailed instructions on how to trigger batch jobs, update the inverted index, and interact with the custom search API.

## Stretch Goals
1. **Advanced Retry Logic and Error Handling**:  
   - Implement robust retry mechanisms, including dead-letter queues and manual intervention strategies.
2. **Enhanced Monitoring**:  
   - Add custom CloudWatch metrics and alerts based on key performance indicators such as TF-IDF processing time and inverted index update latency.
