from django.test import TestCase
from properties.classes.ConnectorProperties import ConnectorProperties
from properties.classes.ConnectorContactRequest import ConnectorContactRequest
from properties.classes.Connector import Connector

class TestClasses(TestCase):

    def setUp(self):
        self.connector_properties = ConnectorProperties('l7u502p8v46ba3ppgvj5y2aad50lb9')
        self.connector = Connector('l7u502p8v46ba3ppgvj5y2aad50lb9')
        self.connector_contact_request = ConnectorContactRequest('l7u502p8v46ba3ppgvj5y2aad50lb9')

# tests for Connector class
    def test_creates_instace_of_connector(self):
        self.assertIsInstance(self.connector, Connector)
        self.assertEqual(self.connector.url, 'https://api.stagingeb.com/v1/')

# tests for ConnectorProperties class

    # test for get_properties_page method
    def test_get_15_properties_page_1(self):
        response = self.connector_properties.get_properties_page(page = 1, limit = 15)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['content']), 15)

    def test_get_15_properties_page_2_just_published(self):
        response = self.connector_properties.get_properties_page(page = 2, limit = 15, statuses=['published'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['content']), 15)
    
    def test_wrong_key(self):
        connector_properties2 = ConnectorProperties('l7u502p8v46ba3ppgvj5y2')
        response = connector_properties2.get_properties_page(page = 1, limit = 15)
        self.assertEqual(response.status_code, 401)

    # test for get_property method
    def test_get_a_propertie_by_its_id(self):
        response = self.connector_properties.get_property('EB-C0156')
        self.assertEqual(response.status_code, 200)
    
    def test_propertie_not_found(self):
        response = self.connector_properties.get_property('EK-C0157')
        self.assertEqual(response.status_code, 404)

# tests for ConnectorContactRequest class

    # test for post_contact_request method
    def test_post_contact_request(self):
        response = self.connector_contact_request.post_contact_request(
            name = 'Gerardo',
            phone = '1234567890',
            email = 'gerardo@gmail.com',
            property_id = 'EB-C0156',
            message = 'Me interesa ésta propiedad',
            source = 'my_props.com'
        )
        self.assertEqual(response.status_code, 200)

    def test_wrong_key(self):
        connector_contact_request = ConnectorContactRequest('l7u502p8v46ba3ppgvj')
        response = connector_contact_request.post_contact_request(
            name = 'Gerardo',
            phone = '1234567890',
            email = 'gerardo@gmail.com',
            property_id = 'EB-C0156',
            message = 'Me interesa ésta propiedad',
            source = 'my_props.com'
        )
        self.assertEqual(response.status_code, 401)

    def test_property_not_found(self):
        response = self.connector_contact_request.post_contact_request(
            name = 'Gerardo',
            phone = '1234567890',
            email = 'gerardo@gmail.com',
            property_id = 'EB-XXXXX',
            message = 'Me interesa ésta propiedad',
            source = 'my_props.com'
        )
        self.assertEqual(response.status_code, 404)

    def test_no_data_provided(self):
        response = self.connector_contact_request.post_contact_request(
            name = '',
            phone = '',
            email = '',
            property_id = '',
            message = '',
            source = ''
        )
        self.assertEqual(response.status_code, 422)