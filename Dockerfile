FROM huaweinoah/smarts:v0.4.16

# replace "mesg n || true" as it give ioctl error
RUN sed -i /root/.profile -e 's/mesg n || true/tty -s \&\& mesg n/g'

#grab own code from git repo
RUN apt-get update && apt-get install git -y
RUN cd /home && git clone https://github.com/Rik-Fox/paavi.git /home

# install stabile baselines, numpy and their unfulfilled dependancies
RUN cd /home && pip install -r requirements.txt

# prettify container shell info
RUN echo "export PS1='🐳 \[\033[1;36m\]\u \[\033[1;34m\]\W\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> /root/.bashrc

# start shell in own src code dir not src
RUN echo "cd /home" >> /root/.bashrc

CMD ["/bin/bash"]