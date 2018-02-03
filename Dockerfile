FROM python:3.6.4-slim-stretch 
RUN apt-get update
RUN apt-get install -y git python3-pip
WORKDIR /cameraobscura  
RUN git clone https://github.com/roastingmalware/cameraobscura.git .
RUN python3 -m pip install -r requirements.txt
CMD python3 main.py
EXPOSE 5000