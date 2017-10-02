import requests
import logging
import pprint

SERVER = 'http://xxx:8888'


#See https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/steps-to-create-a-smart-home-skill

def lambda_handler(request, context):
    logging.info(request)
    if request['directive']['header']['namespace'] == 'Alexa.Discovery' and request['directive']['header']['name'] == 'Discover':
        return handle_discovery(request, context)
    else:
        return handle_directive(request, context)

def handle_discovery(request, context):
    header = request['directive']['header']
    header['name'] = "Discover.Response"

    r = requests.post(SERVER + "/get_devices", json=request)
    payload = {'endpoints': r.json()}
    response = {'event': {'header': header, 'payload': payload}}
    return response

def handle_directive(request, context):
    r = requests.post(SERVER + "/handle_action", json=request)
    if r:
        response = {
          "event": {
            "header": {
              "namespace": "Alexa",
              "name": "Response",
              "payloadVersion": "3",
              "messageId": request['directive']['header']['messageId'],
              "correlationToken":  request['directive']['header']['correlationToken']
            },
            "endpoint": {
              "endpointId": request['directive']['endpoint']['endpointId']
            },
            "payload": {}
          }
        }
        return response
    else:
        return None
