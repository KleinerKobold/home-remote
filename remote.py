from flask import Flask, render_template, request
import pathlib
from loguru import logger
import yaml

from . import api

app = Flask(__name__)

config = {}
with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        logger.info(f"config loaded: {config.keys()}")
        logger.info(f"list of devices: {config['devices']}")

client = api.FreeAtHomeApiClient(config)

@app.route('/',methods=['GET'])
def hello():
    
    device_change = request.args.get("device")
    state = request.args.get("state")
    logger.info(f"received [device: {device_change}, state: {state}]")
    if device_change != None and state != None:
        client.switchState(device_change,state)
    devices = config['devices']

    for device in devices:
        device['state'] = client.getState(device['name'])
    
    logger.info(devices)
    return render_template("remotecontrol.html",title="Remote Control", devices=devices)