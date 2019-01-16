FROM balenalib/rpi-raspbian:stretch-20181201

RUN apt-get -qy update && \
    apt-get -qy install python3       \
                        python3-scapy \
                        tcpdump       \
                        nano          \
                        tcpreplay

RUN apt-get -qy install curl

COPY dash.py /usr/local/bin

CMD ["python3", "/usr/local/bin/dash.py"]
