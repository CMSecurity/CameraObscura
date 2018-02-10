import time
from flask import Flask, request

def run(app: Flask, route: object, request: request, sessionId: str):
   time.sleep(float(route["sleep"]["duration"]))