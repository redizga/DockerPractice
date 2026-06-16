#!/bin/sh
docker run \
  -v "$(pwd)/mosquitto:/mosquitto/config" \
  -p 1883:1883 \
  --name mosquitto \
  --network lab2_net \
  --rm \
  eclipse-mosquitto
