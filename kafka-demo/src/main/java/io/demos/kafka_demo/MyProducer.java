package io.demos.kafka_demo;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Map;
import java.util.Properties;
import java.util.concurrent.*;

public class MyProducer {
	  static final String BOOTSTRAP_SERVERS = "localhost:9092";
	  static final String TOPIC = System.getenv("my-topic");
    public static void main(String[] args) throws Exception {        
        Properties props = new Properties();
	    props.put("bootstrap.servers", BOOTSTRAP_SERVERS);
	    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
	    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

	    KafkaProducer<String, String> producer = new KafkaProducer<>(props);
	    
	    	Executors.newSingleThreadScheduledExecutor().scheduleAtFixedRate(()->
          producer.send(new ProducerRecord<>(TOPIC,
                  "key-"+ThreadLocalRandom.current().nextInt(10),
                  "val-"+ThreadLocalRandom.current().nextInt())), 0, 100, TimeUnit.MILLISECONDS);
	    	producer.close();
    }
}
