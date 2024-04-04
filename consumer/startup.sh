#!/bin/bash

# Function to check if Kafka is ready
function wait_for_kafka() {
    echo "Waiting for Kafka to be ready..."
    while ! nc -z kafka 9092; do
        sleep 1
    done
    echo "Kafka is ready."
}

# Wait for Kafka to be ready
wait_for_kafka

# Start the application
exec python consumer.py
