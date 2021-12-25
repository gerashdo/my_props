from .Connector import Connector
import requests

class ConnectorProperties(Connector):

    def __init__(self, key):
        super().__init__(key)
        self.url_extended = f'{self.url}properties'

    def get_properties_page(self, limit = 20, page = 1, statuses = [], search = None, property_types = None ):

        payload = {
            'limit': limit,
            'page': page,
            'search[statuses]': statuses,
            'search[property_types]': property_types,
            'search': search
        }

        return requests.get(self.url_extended, params=payload, headers=self.headers)

    def get_property(self, property_id):
        return requests.get(f'{self.url_extended}/{property_id}', headers=self.headers)
        