
class Connector:

    def __init__(self, key):
        self.url = 'https://api.stagingeb.com/v1/'
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Authorization': key
        }
        