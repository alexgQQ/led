FROM resin/rpi-raspbian:stretch

# Required ===================================

RUN apt-get update && apt-get install -yq \
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

RUN pip3 install --upgrade pip
COPY requirements.txt app/
RUN pip3 install -r app/requirements.txt

# Copy Driver source files
COPY ./lib /leds

# Build LED driver and install
RUN /bin/bash -c 'cd /leds;                  \
                  scons;                     \
                  cd python;                 \
                  python3 ./setup.py build;  \
                  python3 ./setup.py install'

# Source code
# COPY ./app /app

# # Backend LED library == pull from git
# RUN /bin/bash -c 'git clone https://github.com/jgarff/rpi_ws281x.git led'

# # Build
# RUN /bin/bash -c 'cd led;                   \
#                   scons;                    \
#                   cd python;                \
#                   python3 ./setup.py build;  \
#                   python3 ./setup.py install'

# Optional ===================================

# # Needed for Audio Analysis
# TODO: Fix sklearn dependency issue
#   pip3 install -U scikit-learn
#   cc1: some warnings being treated as errors

# RUN /bin/bash -c 'apt-get install -y -q automake          \
#                                         checkinstall      \
#                                         cmake             \
#                                         libtool           \
#                                         sshfs             \
#                                         unzip             \
#                                         v4l-utils         \
#                                         x264              \
#                                         yasm              \
#                                         libav-tools'
#
# RUN /bin/bash -c 'apt-get install -y -q python3-matplotlib  \
#                                         python3-scipy'
#
# RUN /bin/bash -c 'pip3 install -U scikit-learn'
# RUN /bin/bash -c 'python3 -m pip install hmmlearn simplejson eyed3 pydub'
#
# RUN /bin/bash -c 'git clone https://github.com/tyiannak/pyAudioAnalysis.git paa; \
#                   cd paa;                                                        \
#                   python3 -m pip install -e .'

