# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module contains logging functionality
"""

import time
from datetime import datetime
from os import listdir, stat
from os.path import isfile, join, isabs
from shutil import move
from jsonpickle import encode
from core import config

EVENT_ID_STARTED = "obscura.sensor.started"
EVENT_ID_HTTP = "obscura.sensor.http"
EVENT_ID_HTTP_REQUEST = "obscura.http.request"
EVENT_ID_LOGIN = "obscura.http.login"
EVENT_ID_UPLOAD = "obscura.http.upload"
EVENT_ID_ACTION_NOT_FOUND = "obscura.http.actionnotfound"


class LogEntry():
    """
    Represents a event entry in log
    """
    eventId: ""
    timestamp: None
    message: ""
    isError: 0
    src_ip: ""
    sensor: ""
    kwargs: None

    def __init__(self, eventId: str, timestamp: datetime, message: str,
                 isError: bool, src_ip: str, sensor: str, **kwargs):
        self.eventId = eventId
        self.timestamp = timestamp
        self.message = message
        self.isError = isError
        self.src_ip = src_ip
        self.sensor = sensor
        self.kwargs = kwargs

    def __repr__(self):
        return "[{0}, {1}] {2}: {3} {4}@{5}".format(
            self.timestamp, self.duration, self.eventId, self.message, self.src_ip, self.sensor)


def log(eventId: str, timestamp: datetime, message: str, 
        isError: bool, src_ip: str, **kwargs) -> bool:
    """
    Logs an event
    """
    sensor = config.getConfigurationValue("honeypot", "sensor")
    entry = LogEntry(eventId, timestamp, message,
                     isError, src_ip, sensor, **kwargs)
    selectedLogMethod = config.getConfigurationValue("log", "method")
    # allow only whitelisted method calls
    if selectedLogMethod is not None and selectedLogMethod in [
            "json", "stdout", "text"]:
        return globals()[selectedLogMethod](entry)

    return False


def stdout(entry: LogEntry) -> bool:
    """
    Protocol entry
    @param entry: the log entry to protocol
    @return: operation success state
    """
    print(entry)
    return True


def getLogPath(filename: str) -> str:
    """
    Get the log file path depending on the configuration
    """
    if isabs(filename):
        return filename
    return join(config.ROOT, filename)


def getRotatedLogFilename() -> str:
    """
    gets the rotated filename, e. g. obscura.log.1
    """
    path = config.getConfigurationValue("log", "path")
    completePath = getLogPath(path)
    now = int(time.time())
    if isfile(completePath):
        modification = int(stat(completePath).st_mtime)
    else:
        modification = now - 1  # to trigger creation
    timespan = int(config.getConfigurationValue("log", "timespan"))
    if modification + timespan < now:
        files = ([name for name in listdir('.')
                  if isfile(name) and path in name])
        suffix = len(files)
        move(completePath, completePath + "." + str(suffix))
    return completePath


def json(entry: LogEntry) -> bool:
    """
    Protocol entry
    @param entry: the log entry to protocol
    @return: operation success state
    """
    result = True
    content = encodeLogEntry(entry)
    path = getRotatedLogFilename()
    try:
        with open(path, 'a') as f:
            f.write(content + "\n")
    except FileNotFoundError as e:
        print(e)
        result = False
    return result


def text(entry: LogEntry) -> bool:
    """
    Protocol entry
    @param entry: the log entry to protocol
    @return: operation success state
    """
    result = True
    path = getRotatedLogFilename()
    try:
        with open(path, 'a') as f:
            f.write(entry + "\n")
    except FileNotFoundError as e:
        result = False
        print(e)
    return result


def encodeLogEntry(logEntry: LogEntry) -> str:
    """
    Encodes a log Entry to JSON
    @param entry: the log entry
    @return: the JSON string
    """
    raw = logEntry.__dict__
    if logEntry.kwargs != {}:
        for key, value in logEntry.kwargs.items():
            raw[key] = value

    del logEntry.kwargs
    
    return encode(logEntry, unpicklable=False)
