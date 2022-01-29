from flask import Flask, render_template, request
import pathlib
from loguru import logger
import yaml
import requests


app = Flask(__name__)

with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        logger.info(f"config loaded: {config.keys()}")
        logger.info(f"list of devices: {config['devices']}")



def build_url(device, channel, datapoint):
    return f"http://{config['user']}:{config['password']}@{config['host']}/fhapi/v1/api/rest/datapoint/{config['ap']}/{device}.{channel}.{datapoint}"



def switchState(device:str, state: int):
    url = build_url(device, config['channel'], config['switch']) 
    data = str(state)
    logger.info(f"Switch State {url} to state {data}")
    r = requests.put(url = url, data = data) 
    response_text = r.text
    logger.debug(f"Server response {response_text} {r}")

def explodeResponse(response_text):
    response = yaml.load(response_text, Loader=yaml.FullLoader)
    values = iter(response.values())
    return next(values)['values'][0]

def getState(device:str):
    url = build_url(device, config['channel'], config['state'])
    r = requests.get(url = url) 
    response_text = r.text
    logger.debug(f"Server response on device {device} is {response_text} {r}")
    return explodeResponse(response_text)


@app.route('/',methods=['GET'])
def hello():
    
    device_change = request.args.get("device")
    state = request.args.get("state")
    logger.info(f"received [device: {device_change}, state: {state}]")
    if device_change != None and state != None:
        switchState(device_change,state)
    devices = config['devices']

    for device in devices:
        device['state'] = getState(device['name'])
    
    logger.info(devices)
    return render_template("remotecontrol.html",title="Remote Control", devices=devices)