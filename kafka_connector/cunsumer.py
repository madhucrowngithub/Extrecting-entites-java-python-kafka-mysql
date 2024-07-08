from confluent_kafka import Consumer, KafkaException

# Kafka configuration
consumer_config = {
    'bootstrap.servers': 'localhost:29092',  # Kafka broker address
    'group.id': 'my_consumer_group',        # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start reading at the earliest message
}

# Create Consumer instance
consumer = Consumer(consumer_config)

# Subscribe to topic
consumer.subscribe(['my_topic'])

# Poll for new messages
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break
        print(f"Consumed record with key {msg.key()} and value {msg.value()}")
except KeyboardInterrupt:
    pass
finally:
    # Close down consumer to commit final offsets.
    consumer.close()