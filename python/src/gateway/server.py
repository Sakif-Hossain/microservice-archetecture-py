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