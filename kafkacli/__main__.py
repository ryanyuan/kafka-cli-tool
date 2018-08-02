#!/usr/bin/env python
import argparse
import threading, logging, time
import multiprocessing
import ConfigParser
import sys
from kafka import KafkaConsumer, KafkaProducer

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):

        producer = KafkaProducer(bootstrap_servers=options.broker,
                                 retries=5)

        while not self.stop_event.is_set():
            user_input = raw_input()
            producer.send(options.topic, user_input)

        producer.close()

class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        
    def stop(self):
        self.stop_event.set()
        
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=options.broker,
                                 auto_offset_reset=options.offset,
                                 consumer_timeout_ms=1000)
        consumer.subscribe([options.topic])

        while not self.stop_event.is_set():
            for message in consumer:
                print(message.value)
                if self.stop_event.is_set():
                    break

        consumer.close()
        

def get_topics():
    return KafkaConsumer(bootstrap_servers=options.broker).topics()
    
def print_dashed_line():
    print("---------------------------------------------------")


def main():
    parser = argparse.ArgumentParser(description='''kafkacli - Apache Kafka utility tool''')
    parser.add_argument('-m', required=True, dest='mode', help="Mode: consume, produce, list")
    parser.add_argument('-b', dest='broker', help="Kafka broker endpoint")
    parser.add_argument('-t', dest='topic', help="Topic")
    parser.add_argument('-o', dest='offset', help="Offset mode: earliest, latest (Default: 'latest')")
    
    global options
    options = parser.parse_args()

    if options.mode not in ["Consume", "Produce", "List"] :
        print "Please provide one of the following modes: Consume, Produce, List"
        sys.exit(1)

    print_dashed_line()
    print("Mode: %s" % options.mode)
    print("Broker: %s" % options.broker)
    
    task = None

    if options.mode == "produce":
        print("Topic: %s" % options.topic)
        print_dashed_line()
        task = Producer()
        task.start()
        task.join()
    elif options.mode == "consume":
        print("Offset: %s" % options.offset)
        print("Topic: %s" % options.topic)
        print_dashed_line()
        task = Consumer()
        task.start()
        task.join()
    elif options.mode == "list":
        print_dashed_line()
        topics = get_topics()
        print("\n".join(str(topic) for topic in topics))
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()