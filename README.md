URI Shortener Application
Overview
This document provides detailed instructions for setting up, testing, and deploying the URI Shortener application. The application is containerized using Docker and orchestrated with Docker swarm, with support for Kubernetes for a robust and scalable deployment.

##Prerequisites##
Docker
Kubernetes cluster
kubectl installed and configured
Docker Compose (for local testing)
Local Setup
Clone the Repository

#bash
git clone https://github.com/CyberChrist010/AngiTakeHome/master/)
cd uri-shortener

Build the Docker Image

#bash
docker build -t uri-shortener:latest .

Run the Application Locally
Using Docker Compose:

#bash (ensure docker swarm is started)
docker-compose up
This starts the application on localhost:5001.

##Testing (See test/ directory in the master repo for test app.py and test case commands)

##Kubernetes Deployment##
Create Kubernetes Manifests
In the k8s/ directory, include:

deployment.yaml: Kubernetes deployment configuration
service.yaml: Service configuration
ingress.yaml: Ingress configuration
Deploy to Kubernetes Cluster

#bash
kubectl apply -f k8s/
Verify Deployment

#bash
kubectl get all
Accessing the Application
Find the External IP

#bash
kubectl get svc uri-shortener-service
Interact with the API
Replace [EXTERNAL-IP] with the service's external IP.

#bash

curl -X POST http://[EXTERNAL-IP]:5001/register -H "Content-Type: application/json" -d '{"username":"testuser", "password":"testpass"}'


For additional support or inquiries, please contact: Aaron Stroup @ aaronstrouptech@gmail.com

