FROM python:3.6.4-slim-stretch 
RUN apt-get update
RUN apt-get install -y git python3-pip wget 
WORKDIR /cameraobscura  
RUN git clone https://github.com/roastingmalware/cameraobscura.git .
RUN cp configuration.cfg.dist configuration.cfg
RUN python3 -m pip install -r requirements.txt
EXPOSE 8080
CMD python3 main.py