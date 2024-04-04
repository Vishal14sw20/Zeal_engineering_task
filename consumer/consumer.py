from datetime import datetime

from kafka import KafkaProducer, KafkaConsumer
import psycopg2
import json
import time
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

database_url = os.getenv('DATABASE_URL')

# Kafka consumer setup
consumer = KafkaConsumer('user_interactions',
                         bootstrap_servers='kafka:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))


def create_conn_and_table():
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    # create table if not exists
    try:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS user_interaction_aggregates (
                    user_id INT PRIMARY KEY,
                    login_count INT,
                    logout_count INT,
                    purchase_count INT,
                    aggregation_time TIMESTAMP
                )
            """)
    except psycopg2.Error as e:
        logging.error(f"Error creating table: {e}")

    return conn, cur


def process_events():
    aggregated_data = {}
    start_time = time.time()
    for message in consumer:
        event = message.value
        event_id = event['event_id']
        user_id = event['user_id']
        action = event['action']
        timestamp = event['timestamp']

        # Log the event ID and timestamp for debugging or tracking purposes
        logging.info(f"Processing event: {event_id}, Timestamp: {timestamp}")

        # Aggregate data by user and action
        if user_id not in aggregated_data:
            aggregated_data[user_id] = {'actions': {}, 'timestamp': timestamp}
        if action not in aggregated_data[user_id]['actions']:
            aggregated_data[user_id]['actions'][action] = 0
        aggregated_data[user_id]['actions'][action] += 1
        logging.info(f"Event consumed: {event}")

        # Check if a time window has passed and store aggregated data
        if time.time() - start_time >= 300:  # after 5 minutes
            store_aggregated_data(aggregated_data)
            aggregated_data = {}
            start_time = time.time()


def store_aggregated_data(data):
    for user_id, user_data in data.items():
        actions = user_data['actions']
        login_count = actions.get('login', 0)
        logout_count = actions.get('logout', 0)
        purchase_count = actions.get('purchase', 0)
        timestamp = user_data['timestamp']

        formatted_timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        cur.execute("""
            INSERT INTO user_interaction_aggregates (user_id, login_count, logout_count, purchase_count, aggregation_time)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET login_count = user_interaction_aggregates.login_count + EXCLUDED.login_count,
                logout_count = user_interaction_aggregates.logout_count + EXCLUDED.logout_count,
                purchase_count = user_interaction_aggregates.purchase_count + EXCLUDED.purchase_count,
                aggregation_time = EXCLUDED.aggregation_time
        """, (user_id, login_count, logout_count, purchase_count, formatted_timestamp))
        logging.info(f"Data inserted/updated: {user_id},{actions}, Timestamp: {formatted_timestamp}")

    conn.commit()


if __name__ == "__main__":
    conn, cur = create_conn_and_table()

    process_events()

    # close database connection
    cur.close()
    conn.close()
