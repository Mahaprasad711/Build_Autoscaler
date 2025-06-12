#!/bin/sh

echo "Waiting for server to start on port 8001..."

# Loop until we can connect to the server
while ! nc -z resnet-server-service 8001; do
  sleep 1
done

echo "Server is up - starting client"
python client.py
