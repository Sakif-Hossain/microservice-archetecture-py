CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'auth_password';

CREATE DATABASE auth_db;

GRANT ALL PRIVILEGES ON auth_db.* TO 'auth_user'@'localhost';

USE auth_db;

-- Create the user table
CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('sheikh@email.com', 'admin1234');