# library imports
import os, pika, json, gridfs # gridfs is a library for storing large files in MongoDB
                              # pika is a library for RabbitMQ to store messages  
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
# user imports
from auth import validate
from auth_service import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos" # Endpoint for MongoDB

mongo_videos = PyMongo(
    server,
    uri="mongodb://host.minikube.internal:27017/videos"
)

mongo_mp3 = PyMongo(
    server,
    uri="mongodb://host.minikube.internal:27017/mp3s"
)

fs_videos = gridfs.GridFS(mongo_videos.db) # GridFS object to store large files in MongoDB in chunks
fs_mp3s = gridfs.GridFS(mongo_mp3.db) # GridFS object to store large files in MongoDB in chunks

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")) # Connection to RabbitMQ
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    
    if not err:
        return token
    else:
        return err
    
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request) # Access token is the JSON object of the payload of the JWT token

    if err:
        return err
    
    access = json.loads(access) # Convert the JSON object to a Python dictionary

    if access["is_admin"]:
        # If the user is an admin, then they can upload the video
        if len(request.files) > 1 or len(request.files) < 1:
            return "Please provide exactly one video file", 400

        for _,f in request.files.items():
            err = util.upload(f, fs_videos, access, channel) # Upload the video file to MongoDB

            if err:
                return err
            
        return "Video uploaded successfully", 200
    else:
        return "Unauthorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request) # Access token is the JSON object of the payload of the JWT token

    if err:
        return err
    
    access = json.loads(access) # Convert the JSON object to a Python dictionary

    if access["is_admin"]:
        # If the user is an admin, then they can download the mp3 file
        file_id_string = request.args.get("fid")
        if not file_id_string:
            return "Please provide the file ID", 400
        
        try:
            out = fs_mp3s.get(ObjectId(file_id_string)) # Get the mp3 file from MongoDB
            return send_file(out, download_name=f"{file_id_string}.mp3") # Send the mp3 file to the user
        except Exception as e:
            print(e)
            return "Internal server error /downlad", 500
        

    return "Unauthorized", 401

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)