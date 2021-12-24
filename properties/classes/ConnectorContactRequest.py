from .Connector import Connector
import requests

class ConnectorContactRequest(Connector):

    def __init__(self, key):
        super().__init__(key)
        self.url_extended = f'{self.url}contact_requests'

    def post_contact_request(self, name = '', phone = '', email = '', property_id = '', message ='', source = ''):

        payload = {
            "name": name,
            "phone": phone,
            "email": email,
            "property_id": property_id,
            "message": message,
            "source": source
        }

        return requests.post(self.url_extended, json=payload, headers=self.headers)