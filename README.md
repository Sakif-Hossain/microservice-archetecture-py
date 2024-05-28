# Video to Audio File Conversion Application

The project utilizes a microservice architecture, featuring a gateway service, authentication service, notification service, and conversion service. The gateway service serves as the entry point, routing user requests to the appropriate service.

To ensure scalability and efficient management of a large user base, I containerized the application using Docker and created multiple services with Kubernetes. For inter-service communication, I implemented RabbitMQ, facilitating efficient message passing between services.

[DEMONSTRATION VIDEO](https://youtu.be/V-iqKpMuOak)

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Installation

### Prerequisites
Before you begin, ensure you have the following software installed on your machine:

1. Python3
2. Docker 
3. Kubernetes
4. Minikube
5. RabbitMQ
6. MySQL
7. MongoDB

### Steps
1. ```
   git clone https://github.com/Sakif-Hossain/microservice-archetecture-py.git
   cd microservice-archetecture-py
   ```
2. ```
   minikube start
   minikube addons enable ingress
   minikube tunnel
   ```
3. ```
   cd ./python/src
   kubectl apply -f ./auth/manifests ./converter/manifests ./gateway/manifests ./notification/manifests ./rabbit/manifests
   ```

## Usage

Use cURL to send requests.

```python
# Login using basic authentication
curl -X POST http://mp3converter.com/login -u sheikhshossain02@gmail.com:admin1234

# Copy paste the JWT after Bearer and specify the path of the file
curl -X POST -F 'file=@./file.mp4' -H 'Authorization: Bearer ' http://mp3converter.com/upload

# Add the JWT and fid (from the email)
curl --output something.mp3 -X GET -H 'Authorization: Bearer ' "http://mp3converter.com/download?fid="
```

## Features
- Gateway Service:
  - Acts as the central entry point to the microservices architecture.
  - Routes and redirects user requests to the appropriate service.

- Authentication Service:
  - Manages user login, authentication, and validation.
  - Ensures secure access to services with JWT tokens.

- Notification Service:
  - Handles sending notifications via different channels (e.g., email, SMS).
  - Supports asynchronous message processing for efficiency.

- Conversion Service:
  - Provides functionality for converting Video to Audio files.

- Containerization with Docker:
  - Each service is containerized using Docker for consistent environments.
  - Simplifies deployment and scaling of services.

- Service Created with Kubernetes:
  - Uses Kubernetes for managing and scaling services.
  - Ensures high availability and load balancing across the cluster.

- Efficient Inter-Service Communication with RabbitMQ:
  - Implements RabbitMQ for robust and reliable message queuing.

- Scalability and Reliability:
  - Designed to handle a large user base and high traffic.
  - Utilizes MongoDb Gridfs to allow large media files to be uploaded in chunks.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Contact
Author - Sheikh Safwan Hossain

Email - sakifhossain71@gmail.com

Project Link: [GitHub Repository](https://github.com/Sakif-Hossain/microservice-archetecture-py)

## Acknowledgements
[feeCodeCamp.org](https://youtu.be/hmkF77F9TLw?si=A5xYyw0eEAwnxRgU)
