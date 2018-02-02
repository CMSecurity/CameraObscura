from flask import Flask
from core import config
app = Flask(__name__)

@app.route('/')
def hello():
    cfg=config.getConfigValue("honeypot", "hostname")
    if cfg == None:
        return "nix"
    else:
        return cfg

if __name__ == '__main__':
    app.run(
        debug=True
    )