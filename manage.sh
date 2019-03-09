#!/bin/bash
case "$1" in
    build)
        echo 'Building latest image...'
        docker build -t led-control:latest .
        ;;
    test)
        echo 'Running local tests...'
        docker run --rm -it --privileged --mount type=bind,source=${PWD}/app,target=/app led-control:latest python3 /app/tests.py
        ;;
    install)
        echo 'Installing base deps ...'
        sudo apt-get update -yq && sudo apt-get install -yq \
            python3 \
            python3-dev \
            python3-pip --no-install-recommends \
            python3-numpy \
            build-essential \
            libjpeg-dev \
            swig    \
            scons   \
            git \
            libcairo2-dev \
            pkg-config
        
        pip3 install --upgrade pip
        pip3 install -r requirements.txt

        cd /libs
        scons
        python3 python/setup.py build
        python3 python/setup.py install
        ;;
    *) # Catch unsupported args
        echo "Error: Unsupported flag $1"
        ;;
esac
