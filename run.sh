#!/bin/bash

cleanup() {
  echo "Cleaning up containers..."
  docker-compose down
  exit
}

trap cleanup SIGINT EXIT
docker-compose up --build
