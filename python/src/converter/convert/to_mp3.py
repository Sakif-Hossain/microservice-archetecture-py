import pika, os, json, tempfile
from bson.objectid import ObjectId
import moviepy.editor as mp

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message) # Convert the JSON object to a Python dictionary
    
    # create empty temporary file to store the video file
    temp_file = tempfile.NamedTemporaryFile()
    # get the video file from MongoDB
    out_file = fs_videos.get(ObjectId(message['video_file_id']))
    # write the video file to the temporary file
    temp_file.write(out_file.read())
    # create audio file from the video file
    audio = mp.editor.VideoFileClip(temp_file.name).audio
    # close temporary file
    temp_file.close() # automatically deletes the temporary file aswell

    # write the audio to a file
    temp_file_path = tempfile.gettempdir() + f"/{message['video_file_id']}.mp3"
    audio.write_audiofile(temp_file_path)

    # save the audio file to MongoDB
    f = open(temp_file_path, "rb")
    data = f.read()
    mp3_file_id = fs_mp3s.put(data)
    f.close()
    os.remove(temp_file_path) # remove the temporary file manually since audio.write_audiofile does not delete the file

    # send a message to RabbitMQ to notify the gateway that the audio file is ready
    message["mp3_file_id"] = str(mp3_file_id)
    # send the message to the gateway
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
    except Exception as e:
        fs_mp3s.delete(mp3_file_id)
        return "failed to publish message"