from flask import Flask, request, Response, jsonify

import pprint
import os


app = Flask(__name__)


class Device:
    mapping = {}

    @classmethod
    def device_by_id(cls, id):
        return cls.mapping[id]

    @classmethod
    def get_all(cls):
        return cls.mapping.values()


class WirelessSocketDevice:
    def __init__(self, id, friendly_name, socket_id):
        self.friendly_name = friendly_name
        self.id = id
        self.socket_id = socket_id
        Device.mapping[id] = self

    def get_endpoint_repr(self):
        return {
            "endpointId": self.id,
            "manufacturerName": "Foo",
            "friendlyName": self.friendly_name,
            "description": "",
            "displayCategories": [],
            "cookie": {},
            "capabilities":
                [
                    {
                        "interface": "Alexa.PowerController",
                        "version": "1.0",
                        "type": "AlexaInterface"
                    },

                ]
        }

    def handle_power_on(self):
        print("powering on", self.friendly_name)
        com = "sudo /usr/bin/send 10001 %s 1" % self.id
        os.system(com)

    def handle_power_off(self):
        print("powering off", self.friendly_name)
        com = "sudo /usr/bin/send 10001 %s 0" % self.id
        os.system(com)

    def handle_action(self, action_tuple):
        if ('Alexa.PowerController', 'TurnOn') == action_tuple:
            self.handle_power_on()

        elif ('Alexa.PowerController', 'TurnOff') == action_tuple:
            self.handle_power_off()



WirelessSocketDevice("couchtischlampe", "Couchtischlampe", 1)
WirelessSocketDevice("rechte_stehlampe", "rechte Stehlampe", 2)
WirelessSocketDevice("kleine_lampe", "Kleine Lampe", 3)
WirelessSocketDevice("treppenlampe", "Treppenlampe", 4)
WirelessSocketDevice("schlafzimmerlampe", "Schlafzimmerlampe", 5)


@app.route("/get_devices", methods=["POST"])
def get_devices():
    return jsonify([device.get_endpoint_repr() for device in Device.get_all()])


@app.route("/handle_action", methods=["POST"])
def handle_action():
    data = request.get_json()
    namespace = data['directive']['header']['namespace']
    name = data['directive']['header']['name']
    payload = data['directive']['payload']

    ep = data['directive']['endpoint']['endpointId']

    device = Device.device_by_id(ep)
    device.handle_action((namespace, name))

    return Response("OK", status=200, mimetype='test/html')

app.run(host='0.0.0.0', port=8888, debug=True)
