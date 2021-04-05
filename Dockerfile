#
# Intermediate Compile Image
#

FROM python:3-alpine AS compile-image

RUN apk add --no-cache build-base

RUN python -m venv /opt/venv

# Basically this is everything import <venv>/bin/activate does
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


#
# Final Build Image
#

FROM python:3-alpine AS build-image
COPY --from=compile-image /opt/venv /opt/venv

WORKDIR /cameraobscura

RUN apk add --no-cache shadow; \
    groupadd -r obscura && useradd -r -g obscura -d /cameraobscura -s /sbin/nologin -c "Docker image user" obscura; \
    chown -R obscura:obscura .; \
    apk del --no-cache shadow

USER obscura

COPY . .

EXPOSE 8080

ENTRYPOINT [ "/opt/venv/bin/python3" ]

CMD [ "main.py" ]
