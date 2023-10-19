import requests


class LightsManager:

    def __init__(self, bridge, username):
        self.bridge = bridge
        self.username = username

    def get_base_url(self):
        return f"http://{self.bridge}/api/{self.username}"

    def get_lights(self, ):
        return requests.get(f"{self.get_base_url()}/lights").json()

    def get_light(self, id):
        return requests.get(f"{self.get_base_url()}/lights/{id}").json()

    def change_state(self, id, state):
        requests.put(f"{self.get_base_url()}/lights/{id}/state", json=state)

    def turn_on(self, id):
        self.change_state(id, {"on": True})

    def turn_off(self, id):
        self.change_state(id, {"on": False})

    def change_brightness(self, id, brightness):
        self.change_state(id, {"bri": brightness})
