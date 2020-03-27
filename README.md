# TweetSense

## A twitter sentiment analysis tool to evaluate universities based on student satisfaction in Canada

Kafka Setup
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```
```
bin/kafka-server-start.sh config/server.properties
```
```
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweet
```
Start the producer for getting tweets
```
python tweet_producer.py
```
Check the tweets being produced in real time
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic tweet --from-beginning
```
Running the Stream Analysis Program
```
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0 app.py
```
Dump history tweets
```
python dump_history_tweet.py
```