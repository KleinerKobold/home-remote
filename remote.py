from flask import Flask, render_template, request
import pathlib
from loguru import logger
import yaml
import requests


app = Flask(__name__)

with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        logger.info(f"config loaded: {config.keys()}")

def switchState(device:str, state: int):
    url = f"http://{config['user']}:{config['password']}@{config['host']}/fhapi/v1/api/rest/datapoint/{config['ap']}/{device}.{config['channel']}.{config['switch']}"  
    data = str(state)
    logger.info(f"Switch State {url} to state {data}")
    r = requests.put(url = url, data = data) 
    response_text = r.text
    logger.debug(f"Server response {response_text} {r}")
    


@app.route('/',methods=['GET'])
def hello():
    
    device = request.args.get("device")
    state = request.args.get("state")
    logger.info(f"received [device: {device}, state: {state}]")
    if device != None and state != None:
        switchState(device,state)

    return render_template("remotecontrol.html",title="Remote Control")