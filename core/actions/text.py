
from flask import Flask, request
def run(app: Flask, route: object, request: request, sessionId: str):
  return route["text"]["text"]