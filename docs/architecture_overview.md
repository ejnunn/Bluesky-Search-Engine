# Architecture Overview

## System Architecture Diagram
[Placeholder for architecture diagram]
*(An initial diagram should be added here to visually represent the flow between the various services.)*

## Microservices Design and Responsibilities

- **Data Ingestion Service:**
  - Connects to the Bluesky API to fetch posts.
  - Preprocesses and publishes posts to a Kafka topic for further processing.

- **TF-IDF Processor:**
  - Consumes data from Kafka.
  - Utilizes Apache Hadoop to run MapReduce jobs for computing TF-IDF scores.

- **Search Engine:**
  - Uses Elasticsearch on EC2 to index the processed data.
  - Provides a fast querying mechanism for the frontend.

- **Batch Processing:**
  - AWS Lambda functions, triggered by EventBridge, manage periodic data ingestion and processing.
  - Ensures that the search index is regularly updated with new data.

- **Frontend:**
  - A React-based user interface served as static files from AWS S3 and distributed via CloudFront.
  - Interacts with the backend API to perform searches and display results.

This modular microservices architecture ensures scalability, fault tolerance, and flexibility in deploying and upgrading individual components.
