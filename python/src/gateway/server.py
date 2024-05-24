# library imports
import os, pika, json, gridfs # gridfs is a library for storing large files in MongoDB
                              # pika is a library for RabbitMQ to store messages  
from flask import Flask, request
from flask_pymongo import PyMongo
# user imports
from auth import validate
from auth_service import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos" # Endpoint for MongoDB

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db) # GridFS object to store large files in MongoDB in chunks

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
            err = util.upload(f, fs, access, channel) # Upload the video file to MongoDB

            if err:
                return err
            
        return "Video uploaded successfully", 200
    else:
        return "Unauthorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)