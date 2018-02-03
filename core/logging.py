# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module contains logging functionality
"""

from enum import Enum
from datetime import datetime
from jsonpickle import encode
from core import config

EVENT_ID_STARTED="obscura.sensor.started"

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
  print(entry)
  return True

def json(entry: LogEntry) -> bool:
  content = encodeLogEntry(entry)
  result = True
  try: 
    with open("obscura.json", 'a') as f:
      f.write(content + "\n")
  except (Exception):
    result = False
  return result

def text(entry: LogEntry) -> bool:
  result = True
  try: 
    with open("obscura.json", 'a') as f:
      f.write(entry + "\n")
  except (Exception):
    result = False
  return result

def encodeLogEntry(logEntry: LogEntry) -> str:
  return encode(logEntry, unpicklable=False)