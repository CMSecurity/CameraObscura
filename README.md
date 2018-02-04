# CameraObscura

IP Cam Honeypot

[![Build Status](https://travis-ci.org/RoastingMalware/CameraObscura.svg?branch=master)](https://travis-ci.org/RoastingMalware/CameraObscura)

IP Cameras are often misused for wide range malware campaigns. The purpose of this project is to fake a IP Camera with the common features, such as camera stream, login or firmware upload to protocolize actions done by botnets.

> This project is currently under development. Most of the features are not implemented yet.

## (planned) Features

- [ ] Fake Camera Endpoint (for HTTP `POST`/ `GET` etc.)
  - [ ] Fake camera stream
  - [ ] JSON configurable Routes to simulate logins or upload of new firmware according to the specifications of the manufacturers
  - [ ] Configurable headers to simulate a vulnerable webserver
- [ ] Web Interface
  - [ ] Clone existing to simulate running vulnerable IP-Cams
- [ ] Logging
  - [ ] JSON
  - [ ] Log
  - [ ] SQL
  - [ ] Payload dump (e. g. on fake firmware upload or `POST` with `file`)
- [ ] Fake other services (like RTSP)
  - [ ] RTSP 
  - [ ] SSH/ Telnet (using cowrie)
- [ ] Configuration
  - [ ] Company Logos
  - [ ] Branding
  - [ ] Service/ Port redirect
  - [ ] Routes
- [ ] Deployment/ Analysis/ Usage
  - [ ] CLI Commands (like `start` or `restart`)
  - [ ] Docker Image 
  - [ ] Splunk/ ELK Usage
  - [ ] Upgrade process

## Requirements

Python3

## License

MPL-2.0
