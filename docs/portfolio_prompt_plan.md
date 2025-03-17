# Project Prompts

## Prompt 1: Project Setup and Repository Initialization

**Objective:**
- Initialize a new repository structure for the project.
- Create directories for the backend, frontend, tests, and docs.
- Write an initial README.md that outlines the project overview, architecture, and key components:
  - Data ingestion (pulling posts from Bluesky and pushing to Kafka)
  - TF-IDF processing (using a MapReduce-style job)
  - Custom search engine built with an inverted index (storing precomputed TF-IDF vectors)
  - Batch jobs (scheduled processing via AWS Lambda/EventBridge)
  - Frontend (React-based UI)

**Instructions:**
1. Create the repository layout with the following directories: `/backend`, `/frontend`, `/tests`, and `/docs`.
2. In the `/docs` directory, include an initial architecture overview diagram (it can be a placeholder) and an explanation of the microservices involved.
3. Write a detailed README.md in the root directory that introduces the project, explains the integration of the Bluesky application with a custom TF-IDF search engine using an inverted index, and outlines the planned architecture.

_End this prompt by ensuring that all directories are created and that the README.md provides enough context for future development steps._

---

## Prompt 2: Data Ingestion Service – Bluesky API Integration & Kafka Producer

**Objective:**
- Build a Python microservice that fetches posts from the Bluesky API (or a simulated endpoint) and pushes the data to a Kafka topic.
- Follow test-driven development: write unit tests for both the API client and the Kafka producer.
- Ensure the service is modular and exposes a simple interface for scheduling.

**Instructions:**
1. Create a module (e.g., `data_ingestion.py` inside the `/backend` directory) that includes:
   - A class or function to fetch data from the Bluesky API (or a simulated source).
   - A Kafka producer component that sends the fetched data to a designated Kafka topic.
2. Write unit tests (in `/tests/test_data_ingestion.py`) to verify that:
   - The API client returns the expected data.
   - The Kafka producer correctly formats and sends messages.
3. End with a `main()` function that wires these components together so the service can be invoked as a standalone job.

_Ensure that the code is decoupled to facilitate future integration with the processing pipeline._

---

## Prompt 3: Kafka Setup and Integration

**Objective:**
- Set up Kafka topics and build a simple consumer service to verify message flow.
- Write code to create or validate the existence of required Kafka topics.
- Develop a consumer that listens on the topic and logs incoming messages.
- Include unit tests that simulate message production and consumption.

**Instructions:**
1. Create a module (e.g., `kafka_setup.py` inside the `/backend` directory) that includes:
   - Code to create/configure Kafka topics required by the project.
   - A basic consumer function that subscribes to the topic and prints/logs messages.
2. Write tests (in `/tests/test_kafka.py`) that simulate Kafka message production and consumption.
3. Demonstrate how this component integrates with the data ingestion service (from Prompt 2) by showing interaction between the Kafka producer and consumer.

_End by ensuring that the Kafka configuration and basic messaging flow are verified._

---

## Prompt 4: TF-IDF Processing Service using Hadoop MapReduce

**Objective:**
- Develop a Python-based MapReduce job (simulated or integrated with a local Hadoop cluster) to compute TF-IDF vectors for ingested posts.
- Follow a test-driven approach: write tests for the TF-IDF calculation functions.
- Ensure the module reads messages from Kafka, processes them, and prepares results for indexing into the custom search engine.

**Instructions:**
1. Create a module (e.g., `tfidf_processor.py` inside `/backend`) that implements:
   - Functions to tokenize text, compute term frequency (TF), inverse document frequency (IDF), and combine these into TF-IDF vectors.
   - A MapReduce-like structure (even if simulated) that can process a batch of posts.
2. Write unit tests (in `/tests/test_tfidf.py`) for each function and for the overall TF-IDF vector computation.
3. Conclude by wiring the module with a Kafka consumer (from Prompt 3) so that incoming messages are processed, and the computed TF-IDF vectors are ready for indexing.

_Ensure modularity so the TF-IDF processor can be independently tested and later integrated with the custom inverted index builder._

---

## Prompt 5: Custom Inverted Index Integration for Search Engine

**Objective:**
- Implement code to take the TF-IDF processed results and build a custom inverted index for search.
- Follow best practices by writing tests to verify correct indexing and query responses.
- Design the module to be swappable (e.g., for local development versus deployed environments).

**Instructions:**
1. Create a module (e.g., `search_indexer.py` inside `/backend`) that:
   - Connects to a chosen data store (e.g., a relational database or NoSQL store) for storing the inverted index.
   - Provides functions to index documents by mapping terms to posting lists (document IDs and TF-IDF weights) and to query the index using cosine similarity or another similarity measure.
2. Write integration tests (in `/tests/test_search_indexer.py`) to verify that:
   - Processed TF-IDF vectors are correctly indexed into the inverted index.
   - Query functions return expected results based on custom scoring.
3. Wire this module with the output of the TF-IDF processing service (Prompt 4) so that once TF-IDF vectors are computed, they are automatically indexed.

_End with a complete pipeline connection between TF-IDF output and the custom search engine’s inverted index._

---

## Prompt 6: Batch Processing with AWS Lambda and EventBridge

**Objective:**
- Develop an AWS Lambda function that triggers the entire data pipeline (data ingestion, TF-IDF processing, and indexing into the custom inverted index).
- Configure the Lambda function to be scheduled via AWS EventBridge.
- Implement robust error handling (including retries and logging via CloudWatch).

**Instructions:**
1. Create a module (e.g., `lambda_handler.py` inside `/backend`) that:
   - Invokes the data ingestion service (from Prompt 2).
   - Triggers the TF-IDF processing (from Prompt 4).
   - Calls the custom search indexer (from Prompt 5) to update the inverted index.
2. Include error handling:
   - Wrap each pipeline step with retry logic and log failures to CloudWatch.
   - Write tests (if possible, in `/tests/test_lambda.py`) that simulate failures and verify error handling.
3. End by wiring the function so that it can be scheduled by EventBridge, demonstrating how the entire batch job executes end-to-end.

_Ensure that the Lambda function integrates all components without leaving orphan code._

---

## Prompt 7: Frontend Development with React

**Objective:**
- Create a React-based web frontend that provides a user interface to query the custom search engine.
- Develop components for:
  - Entering search queries.
  - Displaying search results.
  - Handling error states.
- Write tests (unit and integration) for component functionality and API interactions.

**Instructions:**
1. Initialize a new React project (using Create React App or a similar tool).
2. Develop a main component (e.g., `SearchApp.js`) that:
   - Provides an input field for search queries.
   - Fetches results from the public API (which interacts with the backend custom search engine built on the inverted index).
   - Displays results in a list or table.
3. Write component tests (using Jest and React Testing Library) to ensure:
   - Correct API calls.
   - Proper handling of loading and error states.
4. End with wiring the frontend to the backend API, ensuring smooth integration from query submission to result display.

_Make sure that the frontend code is modular and easily testable._

---

## Prompt 8: End-to-End Integration Testing

**Objective:**
- Write comprehensive tests to cover the entire data pipeline—from Bluesky data ingestion through TF-IDF processing, custom inverted index building, and frontend API queries.
- Simulate data flow through Kafka, the TF-IDF processing service, the inverted index creation, and the public API.
- Automate these tests as part of a continuous integration (CI) process.

**Instructions:**
1. Develop integration test scripts (e.g., in `/tests/e2e/`) that:
   - Simulate posting data via the data ingestion service.
   - Validate that the data flows through Kafka and is processed by the TF-IDF service.
   - Confirm that the processed TF-IDF vectors are correctly indexed into the custom inverted index.
   - Verify that a sample query from the frontend returns the expected results.
2. Ensure that tests clean up any test data and simulate failures to validate error handling.
3. End with wiring the tests to run as part of a CI pipeline (using a tool like GitHub Actions or Travis CI).

_The final integration tests should cover all components and ensure that no orphan code remains._

---

## Prompt 9: Deployment Scripts and Monitoring Configuration

**Objective:**
- Develop deployment scripts to provision AWS resources (EC2 or containerized databases for the inverted index, Lambda for batch processing, Kafka setup, etc.) using an Infrastructure-as-Code tool (Terraform or CloudFormation).
- Set up monitoring using AWS CloudWatch for logging, metrics, and alerting.

**Instructions:**
1. Create deployment configuration files (e.g., `terraform/main.tf` or CloudFormation templates) that:
   - Provision the necessary AWS resources: database instance (or container) for the custom inverted index, Lambda functions for batch jobs, and networking.
   - Configure AWS EventBridge to schedule the Lambda functions.
2. Write scripts/configurations to:
   - Enable CloudWatch logging for Lambda functions, the custom search engine, and Kafka.
   - Set up basic alerts for failures or performance issues.
3. End with wiring the deployment configuration with all project components so that a full deployment is possible with a single command.

_Ensure the deployment scripts are well-documented and include testing instructions._

---

## Prompt 10: Documentation, Final Integration, and Developer Onboarding

**Objective:**
- Generate comprehensive documentation that explains the project overview, setup instructions, architecture details, and testing procedures.
- Ensure all previously written code is integrated and that a developer can get started easily.

**Instructions:**
1. Update the README.md to include:
   - A high-level overview of the system architecture.
   - Step-by-step setup instructions for local development and deployment.
   - A section describing the testing strategy (unit, integration, end-to-end).
   - Diagrams or links to architecture visuals (e.g., an ARCHITECTURE.md file).
2. Create additional documentation files in `/docs` as needed, such as:
   - `ARCHITECTURE.md`: Explaining how all microservices interact (data ingestion, TF-IDF processing, inverted index creation, and API querying).
   - `DEPLOYMENT.md`: Detailing how to deploy the system on AWS using the provided deployment scripts.
3. End with wiring all documentation references so that every microservice and integration point is clearly documented.
4. Provide final integration instructions summarizing how a developer can run the full pipeline end-to-end.

_The final documentation should empower any developer to understand, test, and deploy the complete system efficiently._
