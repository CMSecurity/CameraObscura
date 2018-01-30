# CameraObscura

IP Cam Honeypot

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
