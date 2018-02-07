# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module contains logging functionality
"""

from enum import Enum
from datetime import datetime
from jsonpickle import encode
from core import config
from shutil import move
import time
import os
from os.path import dirname, abspath, isfile, join

EVENT_ID_STARTED="obscura.sensor.started"
EVENT_ID_HTTP="obscura.sensor.http"
EVENT_ID_LOGIN="obscura.http.login"
EVENT_ID_UPLOAD="obscura.http.upload"

class LogEntry():
  eventId: ""
  timestamp: None
  message: ""
  system: ""
  isError: 0
  src_ip: ""
  duration: 0.0
  session: None
  sensor: ""
  def __init__(self, eventId: str, timestamp: datetime, message: str, system: str, isError: bool, src_ip: str, duration: float, session: str, sensor: str):
    self.eventId = eventId
    self.timestamp = timestamp
    self.message = message
    self.system = system
    self.isError = isError
    self.src_ip = src_ip
    self.duration = duration
    self.session = session
    self.sensor = sensor
  
  def __repr__(self):
    return "[{0}, {1}] {2}: {3} {4}@{5}".format(self.timestamp, self.duration, self.eventId, self.message, self.src_ip, self.sensor)

def log(eventId: str, timestamp: datetime, message: str, system: str, isError: bool, src_ip: str, duration: float, session: str) -> bool:
  sensor=config.getConfigurationValue("honeypot", "sensor")
  entry=LogEntry(eventId, timestamp, message, system, isError, src_ip, duration, session, sensor)
  selectedLogMethod=config.getConfigurationValue("log","method")
  # allow only whitelisted method calls
  if selectedLogMethod != None and selectedLogMethod in ["json", "stdout", "text"]:
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
  if isfile(filename):
    return filename
  else: 
    return join(config.ROOT, filename)

def json(entry: LogEntry) -> bool: 
  """
  Protocol entry
  @param entry: the log entry to protocol
  @return: operation success state
  """
  content = encodeLogEntry(entry)
  result = True
  path = getLogPath(config.getConfigurationValue("log","path"))
  modification = int(os.stat(path).st_mtime)
  timespan = int(config.getConfigurationValue("log","timespan"))
  now=int(time.time())
  if modification + timespan < now:
    files=([name for name in os.listdir('.') if os.path.isfile(name) and path in name])
    suffix=len(files)
    print("foo")
    move(path, path + "." +  str(suffix))
  try: 
    with open(path, 'a') as f:
      f.write(content + "\n")
  except (Exception):
    result = False
  return result

def text(entry: LogEntry) -> bool:
  """
  Protocol entry
  @param entry: the log entry to protocol
  @return: operation success state
  """
  result = True
  try: 
    path = getLogPath(config.getConfigurationValue("log","path"))
    with open(path, 'a') as f:
      f.write(entry + "\n")
  except (Exception):
    result = False
  return result

def encodeLogEntry(logEntry: LogEntry) -> str:
  """
  Encodes a log Entry to JSON
  @param entry: the log entry
  @return: the JSON string
  """
  return encode(logEntry, unpicklable=False)