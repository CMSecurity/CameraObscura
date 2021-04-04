FROM alpine:latest

WORKDIR /cameraobscura

COPY . .

RUN apk update; \
    apk add build-base python3-dev py3-pip jpeg-dev zlib-dev shadow; \
    LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "python3 -m pip install -r requirements.txt"; \
    groupadd -r obscura && useradd -r -g obscura -d /cameraobscura -s /sbin/nologin -c "Docker image user" obscura; \
    chown obscura:obscura /cameraobscura -R;

EXPOSE 8080
USER obscura

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
