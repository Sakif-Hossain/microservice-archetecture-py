from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import jwt, datetime, os

server = Flask(__name__)
mysql = MySQL(server)

# Config
server.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
server.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "auth_user")
server.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "auth_password")
server.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "auth_db")
server.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", 3306))

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return "Missing username or password", 401

    # Check DB for username and password
    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT email, password FROM user WHERE email = %s", (auth.username,)
    )

    if result > 0:
        data = cursor.fetchone()
        email = data[0]
        password = data[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            token = createJWT(auth.username, os.environ.get("JWT_SECRET", "mysecret"), True)
            return jsonify(token=token)
    else:
        return "User not found", 401

def createJWT(username, secret, is_admin):
    payload = {
        "username": username,
        "is_admin": is_admin,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

@server.route("/validate", methods=["POST"])
def validate():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        return "Token is missing", 401

    token = auth_header.split(" ")[1]

    try:
        decoded = jwt.decode(token, os.environ.get("JWT_SECRET", "mysecret"), algorithms=["HS256"])
        return jsonify(decoded), 200
    except jwt.ExpiredSignatureError:
        return "Token has expired", 403
    except jwt.InvalidTokenError:
        return "Invalid token", 403

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)