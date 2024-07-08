from kafka import KafkaProducer
import logging
import json
import os

# Kafka configuration
# producer_config = {
#     'bootstrap.servers': 'kafka:9092',  # Kafka broker address
# }
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],  
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
# Create Producer instance



# producer = Producer(producer_config)

# Function to handle delivery reports


# def delivery_report(err, msg):
#     if err is not None:
#         print(f"Delivery failed for record {msg.key()}: {err}")
#     else:
#         print(f"Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def push_to_kafka(set_value):
# Produce messages
    try:
        for key, value in set_value.items():
            logging.info(f'pushing data to the kafka to the topic : my_topic  and key : {key} and the value {value}')
        # producer.produce('my_topic', key=key, value=value)
        # producer.poll(0)
         
            producer.send('wordentity', value=value, key=key)
        producer.flush()
    except:
        return 

# for i in range(10):
#     key = f'key-{i}'
#     value = f'value-{i}'
#     producer.produce('my_topic', key=key, value=value, on_delivery=delivery_report)
#     producer.poll(0)

# Wait for any outstanding messages to be delivered
Dict = {1: 'Geeks', 2: 'For', 3: 'Geeks'}
push_to_kafka(Dict)

