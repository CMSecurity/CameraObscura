
import termcolor
import random
import string
import time
from core import config
from os import read
from os.path import join, isfile

def init():
  '''
  firmware=1.5-retail-us
  serial=HX21BZ
  model=C2259
  '''
  mode = random.randint(1,2)
  oldSerial = "HX21BZ"
  oldModel = "C2259"
  oldVersion = "1.5-retail-us"
  oldName = "camera"
  oldHostname="cam04"
  productNames = [
    "IPCAM Viewer",
    "Security CAM",
    "CAM",
    "CCTV",
    "IPCAM",
    "User Interface IP Cam",
    "監控攝像機"
  ]
  hostnames = [
    "camera" + randomString(10),
    "camera" + str(random.randint(1,25)),
    "cam" + str(random.randint(1,25)),
    "cctv",
    "linux",
    "localhost"
  ]

  configPath = join(config.ROOT, "configuration.cfg")
  productName = productNames[random.randint(0, len(productNames) -1)]
  hostName = hostnames[random.randint(0, len(hostnames) -1)]
  if isfile(configPath):
    print(termcolor.colored("Warning: Your config is already initialized. We stop here.", "red"))
    return
  if mode % 2 == 0:
    snLength = random.randint(5, 10)
    serialNumber = ''.join(random.choices(string.ascii_uppercase + string.digits, k=snLength))
    modelNumber =  randomString(2) + "-" + randomString(5)
    versionNumber = str(random.randint(1, 3)) + "." + str(random.randint(1, 3))
  else:
    snLength = random.randint(5, 10)
    serialNumber = ''.join(random.choices(string.digits, k=snLength))
    modelNumber = randomString(random.randint(5,10)) + randomString(2)  
    if int(time.time()) & 10 == 0:
      versionNumber = random.randint(1, 3)
    else:
      versionNumber = str(random.randint(1, 3)) + randomString(5) 
  
  print("SerialNumber will be {0} (was {1})".format(termcolor.colored(serialNumber,"yellow"), oldSerial))
  print("Model will be {0} (was {1})".format(termcolor.colored(modelNumber,"yellow"), oldModel))
  print("Version will be {0} (was {1})".format(termcolor.colored(versionNumber,"yellow"), oldVersion))
  print("Name will be {0} (was {1})".format(termcolor.colored(productName,"yellow"), oldName))
  print("Hostname will be {0} (was {1})".format(termcolor.colored(hostName,"yellow"), oldHostname))


  if isfile(configPath):
    readPath =  join(config.ROOT, "configuration.cfg")
  else:
    readPath = join(config.ROOT, "configuration.cfg.dist") 
  content = ""
  with open(readPath, 'r') as content_file:
    content = content_file.read()
    content = content.replace("model={0}".format(oldModel), "model={0}".format(modelNumber))
    content = content.replace("serial={0}".format(oldSerial), "serial={0}".format(serialNumber))
    content = content.replace("firmware={0}".format(oldVersion), "firmware={0}".format(versionNumber))
    content = content.replace("name={0}".format(oldName), "name={0}".format(productName))
    content = content.replace("hostname={0}".format(oldHostname), "hostname={0}".format(hostName))

  with open(configPath, "w") as text_file:
    text_file.write(content)
  
  print("We wish you a successfull hunt")
def randomString(amount: int) -> str:
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=amount))