import pika, sys, os, time
from send import email

def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq")) # service name resolves to the IP address of the RabbitMQ service
    channel = connection.channel() # start a channel
    
    def callback(ch, method, properties, body):
        err = email.notification(body) # send an email notification
        if err:
            print(err)
            ch.basic_nack(delivery_tag=method.delivery_tag) # negitive acknowledge the message if the conversion fails, keep the message in the queue
        else:
            print("Email sent successfully")
            ch.basic_ack(delivery_tag=method.delivery_tag) # acknowledge the message if the conversion is successful
    
    # Listen from the MP3_QUEUE
    channel.basic_consume(queue=os.environ.get("MP3_QUEUE"), on_message_callback=callback)
    
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