from kafka import KafkaProducer, KafkaConsumer
import json
import time
import random
import logging
import uuid


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka producer setup
producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))




def simulate_data_source():
    while True:
        # Simulate user interaction data
        event = {
            "event_id": str(uuid.uuid4()),  # Generate a unique ID for the event
            "user_id": random.randint(1, 10),
            "action": random.choice(["login", "logout", "purchase"]),
            "timestamp": time.time()
        }
        producer.send('user_interactions', event)
        logging.info(f"Event produced: {event}")
        time.sleep(random.randint(1, 5)) # Send events at irregular intervals





if __name__ == "__main__":
    simulate_data_source()
