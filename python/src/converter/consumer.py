import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def main():
    # Connect to MongoDB
    client = MongoClient("host.minikube.internal", 27017) # Access to host system in local env not in cluster
    # Create a database called videos and mp3s
    db_videos = client.videos
    db_mp3s = client.mp3s
    # Create a GridFS object to store the video and mp3 files
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)
    
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq")) # service name resolves to the IP address of the RabbitMQ service
    channel = connection.channel() # start a channel
    
    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, channel)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag) # negitive acknowledge the message if the conversion fails, keep the message in the queue
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag) # acknowledge the message if the conversion is successful
    
    channel.basic_consume(queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback)
    
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming() # run the consumer

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) # gracefully exit the consumer