# TODO Checklist for Portfolio Project

This checklist outlines all the key steps to build and deploy the integrated Bluesky and custom TF-IDF search engine project. Use it to track your progress and ensure that every component is built, tested, and integrated properly.

---

## 1. Repository Setup and Project Initialization
- [ ] **Create Repository Structure**
  - [ ] Initialize a new repository.
  - [ ] Create the following directories:
    - `/backend`
    - `/frontend`
    - `/tests`
    - `/docs`
- [ ] **Documentation Setup**
  - [ ] Create an initial `README.md` with:
    - Project overview.
    - Architecture description (including data ingestion, TF-IDF processing, custom inverted index search engine, batch jobs, and frontend).
    - List of microservices and components.
  - [ ] Add a placeholder architecture diagram and explanation in `/docs/ARCHITECTURE.md`.
- [ ] **Version Control**
  - [ ] Set up Git configuration.
  - [ ] Make the initial commit with the repository structure and documentation.

---

## 2. Data Ingestion Service: Bluesky API Integration & Kafka Producer
- [ ] **Develop Data Ingestion Module**
  - [ ] Create `backend/data_ingestion.py`:
    - Implement a function/class to fetch posts from the Bluesky API (or a simulated endpoint).
    - Implement a Kafka producer to publish posts to a designated Kafka topic.
- [ ] **Testing**
  - [ ] Write unit tests in `/tests/test_data_ingestion.py` to verify:
    - The API client returns expected data.
    - The Kafka producer correctly formats and sends messages.
- [ ] **Integration**
  - [ ] Wire components together with a `main()` function for standalone execution.

---

## 3. Kafka Setup and Integration
- [ ] **Configure Kafka**
  - [ ] Create `backend/kafka_setup.py`:
    - Write code to create and validate the required Kafka topics.
    - Develop a basic consumer that subscribes to the topic and logs incoming messages.
- [ ] **Testing**
  - [ ] Write unit tests in `/tests/test_kafka.py` to:
    - Simulate Kafka message production.
    - Validate that the consumer processes messages correctly.
- [ ] **Integration**
  - [ ] Connect Kafka configuration with the data ingestion service from Step 2.

---

## 4. TF-IDF Processing Service using Hadoop MapReduce
- [ ] **Develop TF-IDF Processing Module**
  - [ ] Create `backend/tfidf_processor.py`:
    - Implement functions to tokenize text, compute term frequency (TF), inverse document frequency (IDF), and combine these into TF-IDF vectors.
    - Simulate a MapReduce processing pipeline (or integrate with a local Hadoop cluster).
- [ ] **Testing**
  - [ ] Write unit tests in `/tests/test_tfidf.py` for:
    - Each individual function.
    - The overall TF-IDF vector computation process.
- [ ] **Integration**
  - [ ] Wire the TF-IDF module with a Kafka consumer (from Step 3) so that incoming messages are processed.
  - [ ] Prepare the processed TF-IDF vectors for the custom inverted index integration.

---

## 5. Custom Inverted Index Integration for Search Engine
- [ ] **Develop Custom Search Index Module**
  - [ ] Create `backend/search_indexer.py`:
    - Implement connection logic to the chosen data store (e.g., PostgreSQL with JSONB or a NoSQL solution) for storing the inverted index.
    - Develop functions to index documents by mapping terms to posting lists (document IDs and TF-IDF weights).
    - Implement query functions that compute similarity (e.g., cosine similarity) between a query vector and document vectors.
- [ ] **Testing**
  - [ ] Write integration tests in `/tests/test_search_indexer.py` to:
    - Verify that processed TF-IDF vectors are correctly indexed into the inverted index.
    - Validate that query functions return expected results based on custom scoring.
- [ ] **Integration**
  - [ ] Wire this module with the output of the TF-IDF processing service (Step 4) so that TF-IDF vectors are automatically indexed.

---

## 6. Batch Processing with AWS Lambda and EventBridge
- [ ] **Develop Lambda Function**
  - [ ] Create `backend/lambda_handler.py`:
    - Invoke the data ingestion service (Step 2).
    - Trigger the TF-IDF processing (Step 4).
    - Call the custom search indexer (Step 5) to update the inverted index.
- [ ] **Error Handling**
  - [ ] Implement robust error handling:
    - Add retry logic for each pipeline step.
    - Integrate logging via AWS CloudWatch.
- [ ] **Testing**
  - [ ] Write tests in `/tests/test_lambda.py` to simulate pipeline failures and verify error handling.
- [ ] **Integration**
  - [ ] Configure AWS EventBridge to schedule the Lambda function.
  - [ ] Ensure the Lambda function executes the full data pipeline end-to-end.

---

## 7. Frontend Development with React
- [ ] **Initialize Frontend Project**
  - [ ] Create a new React project in `/frontend` (e.g., using Create React App).
- [ ] **Develop Search Interface**
  - [ ] Create the main component (e.g., `frontend/src/SearchApp.js`):
    - Implement an input field for search queries.
    - Fetch search results from the public API that interacts with the custom inverted index.
    - Display results in a list or table.
  - [ ] Handle UI states:
    - Loading indicators.
    - Error messages.
- [ ] **Testing**
  - [ ] Write component tests using Jest and React Testing Library:
    - Test API interactions.
    - Verify proper handling of loading and error states.
- [ ] **Integration**
  - [ ] Connect the frontend with the backend API to complete the search functionality.

---

## 8. End-to-End Integration Testing
- [ ] **Develop Integration Tests**
  - [ ] Create test scripts in `/tests/e2e/` that:
    - Simulate posting data via the data ingestion service.
    - Validate message flow through Kafka.
    - Confirm TF-IDF processing on ingested data.
    - Verify that processed TF-IDF vectors are correctly indexed into the custom inverted index.
    - Ensure that the frontend retrieves and displays the correct search results.
- [ ] **Automation**
  - [ ] Clean up test data after execution.
  - [ ] Integrate these tests into the CI/CD pipeline.

---

## 9. Deployment Scripts and Monitoring Configuration
- [ ] **Deployment Scripts**
  - [ ] Create deployment configurations (using Terraform or CloudFormation) in a `/deployment` directory:
    - Provision the necessary AWS resources: database/containers for the custom inverted index, Lambda functions for batch jobs, Kafka setup (or managed Kafka service), and networking.
    - Configure AWS EventBridge to schedule Lambda executions.
- [ ] **Monitoring and Logging**
  - [ ] Configure AWS CloudWatch for:
    - Logging for Lambda functions, the custom search engine, and Kafka.
    - Monitoring key metrics.
    - Setting up alerts for failures and performance issues.
- [ ] **Documentation**
  - [ ] Document deployment and monitoring setup in `/docs/DEPLOYMENT.md`.

---

## 10. Documentation, Final Integration, and Developer Onboarding
- [ ] **Update Documentation**
  - [ ] Revise `README.md` with:
    - A detailed project overview.
    - Step-by-step setup instructions for local development and deployment.
    - A testing strategy section (unit, integration, end-to-end).
  - [ ] Create additional documentation files:
    - `/docs/ARCHITECTURE.md` detailing microservices and system architecture.
    - `/docs/DEPLOYMENT.md` with deployment and configuration instructions.
- [ ] **Developer Onboarding**
  - [ ] Write onboarding instructions for new developers.
  - [ ] Ensure every microservice and integration point is clearly documented.
- [ ] **Final Integration and Cleanup**
  - [ ] Verify that all components are properly wired together with no orphan code.
  - [ ] Run comprehensive end-to-end tests.
  - [ ] Set up continuous integration (e.g., GitHub Actions, Travis CI) to automate testing.

---
