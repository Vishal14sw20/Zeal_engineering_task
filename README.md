# Real-Time Data Processing Pipeline

This repository contains a setup for a Kafka-Postgres data pipeline, comprising a producer, a consumer, and Grafana for visualization. Below are the setup instructions and how the data is handled:


## Prerequisites

- Docker and Docker Compose installed on your machine.

## Instructions

1. **Clone this repository to your local machine:**

    ```bash
    git clone https://github.com/Vishal14sw20/Zeal_engineering_task.git
    ```

2. **Navigate to the cloned directory:**

    ```bash
    cd <cloned_directory>
    ```

3. **Run the Docker Compose command to spin up the services defined in** `docker-compose.yml`:

    ```bash
    docker-compose up -d
    ```

    This will start Zookeeper, Kafka, Postgres, Producer, Consumer, and Grafana services.

4. **Once the services are up and running, you can access Grafana at** `http://localhost:3000` **in your web browser. Login with default credentials** (admin/admin).

5. **finally, you will see dashboard inside dashboard tab**


## Overview
- The producer service sends sample data to Kafka topics.
- The consumer service retrieves data from Kafka topics and stores it in the PostgreSQL database.
- Grafana reads data from the PostgreSQL database and visualizes it through dashboards.
  - Data source and dashboard configurations are provided in the `grafana-provisioning` directory.
  - Grafana service will mount this directory to the container.

# Data Handling
- **Data Generation:** Data is randomly generated to simulate user interactions, creating event_id, user_id, and action type [logout, login, purchase].
- **Consumer Storage:** The consumer stores the count of different actions performed by each user and the latest time of their action.
- **Grafana Visualization:** Grafana displays the sum of actions performed by each user.


## In Real-World Scenario
This solution serves as a simplified demonstration of a Kafka-Postgres data pipeline with Grafana visualization. In real-world scenarios, several enhancements and modifications would likely be implemented:

- **Directory Structure:** In a production environment, the directory structure might be more complex, with separate folders for SQL scripts, configuration files, and other resources to ensure better organization and maintainability.

- **Container Orchestration:**  Use of Kubernetes for better scalability, reliability, and resource utilization.

- **Automated Testing and CI/CD:** Implementing automated testing practices and CI/CD pipelines.
- **Credentials:** Saved in Vault for security.
- **etc**

