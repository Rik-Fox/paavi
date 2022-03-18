FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

# Prevent tzdata from trying to be interactive
ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
# ENV LANG C.UTF-8

RUN apt-get upgrade --fix-missing

# Install libraries
RUN apt-get update --fix-missing && \
    apt-get install -y \
        software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    add-apt-repository -y ppa:sumo/stable 
# Install libraries
RUN apt-get update --fix-missing && \
    apt-get install -y \
        python3.9 \
        libspatialindex-dev \
        sumo \
        sumo-doc \
        sumo-tools \
        git \
        wget \
        xorg && \ 
# remove hanging packages and repos
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# Setup SUMO
ENV SUMO_HOME /usr/share/sumo

# Update default python version
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1

# Setup virtual environment and install pip
ENV VIRTUAL_ENV=/opt/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py && \
    python get-pip.py && \
    pip install --upgrade pip

# Copy source files and install SMARTS
run git clone https://github.com/Rik-Fox/SMARTS_PAAVI.git /src
WORKDIR /src
RUN pip install --no-cache-dir -e .[train,test,dev,camera-obs] && \
    cp -r /src/smarts.egg-info /media/smarts.egg-info

# For Envision
EXPOSE 8081

RUN git clone https://github.com/Rik-Fox/paavi.git
# COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /paavi/requirements.txt

# Suppress message of missing /dev/input folder and copy smarts.egg-info if not there
RUN echo "mkdir -p /dev/input\n" \
         "if [[ ! -d /src/smarts.egg-info ]]; then" \
         "   cp -r /media/smarts.egg-info /src/smarts.egg-info;" \
         "   chmod -R 777 /src/smarts.egg-info;" \
         "fi" >> ~/.bashrc

# start shell in own src code dir not src
RUN echo "cd /paavi" >> /root/.bashrc

# replace "mesg n || true" as it give ioctl error
# RUN sed -i /root/.profile -e 's/mesg n || true/tty -s \&\& mesg n/g'

# prettify container shell info
RUN echo "export PS1='🐳 \[\033[1;36m\]\u \[\033[1;34m\]\W\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> /root/.bashrc

SHELL ["/bin/bash", "-c", "-l"]

CMD ["/bin/bash"]