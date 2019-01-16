#!bin/bash
docker rm -f dash
docker run --net host -it -v /etc/localtime:/etc/localtime:ro --name dash holgerimbery/amazon-dashbutton-webhook:latest /bin/bash
