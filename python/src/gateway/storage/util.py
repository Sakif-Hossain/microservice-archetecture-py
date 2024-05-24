import pika, json

def upload(file, fs, access, channel):
    """
    The function uploads the file to MongoDB using GridFS, sends a message to RabbitMQ so that downstream services can process the file,
    by pulling it from MongoDB. This allows the asynchronous flow between the gateway and the service that processes the video file.

    1. Upload the file to MongoDB using GridFS
    2. Send a message to RabbitMQ to process the file when the file is uploaded successfully

    Args:
        file (werkzeug.datastructures.FileStorage): The file to be uploaded
        fs (gridfs.GridFS): The GridFS object to store the file in MongoDB
        access (dict): The JSON object of the payload of the JWT token
        channel (pika.channel.Channel): The channel object to send messages to RabbitMQ

    returns:
        str: Error message if the file is not uploaded successfully, None otherwise
    """
    try:
        # Save the file in MongoDB
        file_id = fs.put(file)
    except Exception as e:
        print(e)
        return f"Error saving file to MongoDB: {e}", 500
    
    # Send a message to RabbitMQ to process the file
    message = {
        "video_file_id": str(file_id),
        "mp3_file_id": None,
        "username": access["username"]
    }

    try:
        channel.basic_publish(
            exchange="", 
            routing_key="video", 
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )
    except Exception as e:
        print(e)
        fs.delete(file_id)
        return f"Error publishing message to RabbitMQ: {e}", 500