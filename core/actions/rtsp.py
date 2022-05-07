# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Serves a given file as HTTP response
"""

from flask import Flask, request, Response
import cv2

def gen_frames(camera):
    while True:
        success, frame = camera.read()
        if success:
            _1, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def run(app: Flask, selectedPath: str, route: object,
        request: request):
    stream = route["rtsp"]["stream"]
    camera = cv2.VideoCapture(stream)
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

