import requests
import yaml
from loguru import logger

class FreeAtHomeApiClient():
    def __init__(self, config):
        self.config = config

    def build_url(self, device, channel, datapoint):
        return f"http://{self.config['user']}:{self.config['password']}@{self.config['host']}/fhapi/v1/api/rest/datapoint/{self.config['ap']}/{device}.{channel}.{datapoint}"

    def switchState(self, device:str, state: int):
        url = self.build_url(device, self.config['channel'], self.config['switch']) 
        data = str(state)
        logger.info(f"Switch State {url} to state {data}")
        r = requests.put(url = url, data = data) 
        response_text = r.text
        logger.debug(f"Server response {response_text} {r}")

    def explodeResponse(self, response_text):
        response = yaml.load(response_text, Loader=yaml.FullLoader)
        values = iter(response.values())
        return next(values)['values'][0]

    def getState(self, device:str):
        url = self.build_url(device, self.config['channel'], self.config['state'])
        r = requests.get(url = url) 
        response_text = r.text
        logger.debug(f"Server response on device {device} is {response_text} {r}")
        return self.explodeResponse(response_text)

    def getState(self, device:str):
        url = self.build_url(device, self.config['channel'], self.config['state'])
        r = requests.get(url = url) 
        response_text = r.text
        logger.debug(f"Server response on device {device} is {response_text} {r}")
        return self.explodeResponse(response_text)
