FROM alpine:latest
RUN apk update
RUN apk add build-base python3-dev py3-pip jpeg-dev zlib-dev shadow git
WORKDIR /cameraobscura  
RUN git clone https://github.com/roastingmalware/cameraobscura.git .
RUN LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "python3 -m pip install -r requirements.txt"
EXPOSE 8080
RUN groupadd -r obscura && useradd -r -g obscura -d /cameraobscura -s /sbin/nologin -c "Docker image user" obscura
RUN chmod +x obscura.sh
RUN chown obscura:obscura /cameraobscura -R
USER obscura
CMD python3 main.py
