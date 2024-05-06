from flask import Flask, request
from flask_mysqldb import MySQL
import jwt, datetime, os

server = Flask(__name__)
mysql = MySQL(server)

#config
server.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
server.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD") 
server.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return "Missing username or password", 401
    
    #check DB for username and password
    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT email, password FROM user WHERE email = %s", (auth.username,)
    )

    if result > 0:
        data = cursor.fetchone()
        email = data[0]
        password = data[1]

        if auth.email != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET_KEY"), True)
    else:
        return "User not found", 401
    
def createJWT(username, secret, is_admin):
    payload = {
        "username": username,
        "is_admin": is_admin,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

@server.route("/validate", methods=["POST"])
def validate():
    token = request.headers.get("Authorization")

    if not token:
        return "Token is missing", 401
    
    encoded_token = token.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_token, os.environ.get("JWT_SECRET_KEY"), algorithm=["HS256"])
    except jwt.ExpiredSignatureError:
        return "Token has expired", 403
    except jwt.InvalidTokenError:
        return "Invalid token", 403
    return decoded, 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)