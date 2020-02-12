# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Serves a text as HTTP response
"""
from flask import Flask, request


def run(app: Flask, selectedPath: str, route: object,
        request: request):
    return route["text"]["text"]
