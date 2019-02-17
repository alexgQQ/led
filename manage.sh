#!/bin/bash
case "$1" in
    build)
        echo 'Building latest image...'
        docker build -t led-control:latest .
        ;;
    test) # end argument parsing
        echo 'Running local tests...'
        docker run --rm -it --privileged --mount type=bind,source=${PWD}/app,target=/app led-control:latest python3 /app/tests.py
        ;;
    *) # Catch unsupported args
        echo "Error: Unsupported flag $1"
        ;;
esac
