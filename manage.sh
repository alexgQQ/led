#!/bin/bash
case "$1" in
    build)
        echo 'Building latest image...'
        docker build -t led-control:latest .
        ;;
    test)
        echo 'Running local tests...'
        docker run --rm -it --privileged --mount type=bind,source=${PWD}/app,target=/app led-control:latest python3 -m app.tests.unit_tests
        ;;
    install)
        echo 'Installing base deps ...'
        sudo apt-get update -yq && sudo apt-get install -yq \
            python3 \
            python3-dev \
            python3-pip --no-install-recommends \
            python3-numpy \
            python3-setuptools \
            build-essential \
            libjpeg-dev \
            swig    \
            scons   \
            git \
            libcairo2-dev \
            pkg-config
        
        python3 -m pip install --upgrade pip
        python3 -m pip install -r requirements.txt

        cd lib
        scons
        cd python
        python3 setup.py build
        python3 setup.py install
        ;;
    *) # Catch unsupported args
        echo "Error: Unsupported flag $1"
        ;;
esac
