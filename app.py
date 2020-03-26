from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json


def main():
    sc = SparkContext(appName="tweetsense")

    # Set the Batch Interval is 10 sec of Streaming Context
    ssc = StreamingContext(sc, 10)

    # Create Kafka Stream to Consume Data Comes From Twitter Topic
    # localhost:2181 = Default Zookeeper Consumer Address
    kafkaStream = KafkaUtils.createDirectStream(
        ssc, 
        topics = ['tweet'], 
        kafkaParams = {
            "metadata.broker.list": 'localhost:9092'
        }
    )

    tweets = kafkaStream.map(lambda x: (x[1], "kkk"))

    # Print the User tweet counts
    tweets.pprint()

    # Start Execution of Streams
    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
