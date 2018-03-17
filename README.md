# CameraObscura

IP Cam Honeypot

[![Build Status](https://travis-ci.org/RoastingMalware/CameraObscura.svg?branch=master)](https://travis-ci.org/RoastingMalware/CameraObscura)

IP Cameras are often misused for wide range malware campaigns. The purpose of this project is to fake a IP Camera with the common features, such as camera stream, login or firmware upload to protocolize actions done by botnets.

> This project is currently under development. Most of the features are not implemented yet.

> For God's sake, don't deploy this to productive environments. It's an honeypot which also could be exploited.

## (planned) Features

- [ ] Fake Camera Endpoint (for HTTP `POST`/ `GET` etc.)
  - [ ] Fake camera stream
  - [x] JSON configurable Routes to simulate logins or upload of new firmware according to the specifications of the manufacturers
  - [x] Configurable headers to simulate a vulnerable webserver
- [ ] Web Interface
  - [x] Semi-Fake Web UI
  - [ ] Clone existing to simulate running vulnerable IP-Cams
- [ ] Logging
  - [x] JSON
  - [x] Log (text)
  - [ ] SQL
  - [x] Payload dump (e. g. on fake firmware upload or `POST` with `file`)
- [ ] Fake other services (like RTSP)
  - [ ] RTSP 
  - [ ] SSH/ Telnet (using cowrie)
- [ ] Configuration
  - [x] Company Logos (via config/templates)
  - [x] Branding (via config/ templates)
  - [ ] Service/ Port redirect
  - [x] Routes
- [ ] Deployment/ Analysis/ Usage
  - [ ] CLI Commands (like `start` or `restart`)
  - [ ] Docker Image 
  - [ ] Splunk/ ELK Usage
  - [ ] Upgrade process

## Requirements

Python3

## Recommendations

- Don't run the honeypot as root
- Don't run the honeypot on a productive environment
- Use a dedicated, isolated environment (like `qemu`, `lxd`, `lxc` or `docker`)

## License

MPL-2.0
