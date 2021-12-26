from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.contact_request_data = {
            'name': 'Juan Gonzales',
            'phone': '1234567890',
            'email': 'juan@gmail.com',
            'message': 'Hola, estoy interesado en tu propiedad'
        }
   
# tests for index view
    def test_index_url_withot_parameters(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_url_name(self):
        response = self.client.get(reverse('properties:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_url_with_parameters(self):
        response = self.client.get('/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_last_properties_page_shoul_not_have_next_page_link(self):
        response = self.client.get('/28')
        self.assertNotContains(response, 'Página siguiente')

    def test_first_properties_page_shoul_have_next_page_link(self):
        response = self.client.get('/')
        self.assertContains(response, 'Página siguiente')
    
    def test_first_properties_page_should_have_15_image_tags(self):
        response = self.client.get('/')
        self.assertContains(response, '<img src="', count=15)

# tests for show_property view

    def test_show_property_correct_url_an_template_used(self):
        response = self.client.get('/properties/EB-B5516')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_property.html')

    def test_show_property_url_name(self):
        response = self.client.get(reverse('properties:show_property', args=['EB-B5516']))
        self.assertEqual(response.status_code, 200)

    def test_invalid_property_id(self):
        response = self.client.get('/properties/EB-XXXXX')
        self.assertEqual(response.status_code, 404)

    def test_should_show_default_hause_image_if_property_has_no_one(self):
        response = self.client.get('/properties/EB-C0118')
        self.assertContains(response, '<img src="/static/img/default_house.jpg"')

# tests for process_contact_request view

    def test_contact_request_succesful_post(self):
        response = self.client.post('/properties/EB-B5516', self.contact_request_data)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Tu solicitud ha sido enviada')

    def test_contact_request_no_valid_form(self):
        self.contact_request_data['name'] = ''
        response = self.client.post('/properties/EB-B5516', self.contact_request_data)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Algunos datos no son válidos')

    def test_contact_request_no_valid_form_keep_data_inputs(self):
        self.contact_request_data['name'] = ''
        response = self.client.post('/properties/EB-B5516', self.contact_request_data)
        self.assertContains(response, 'value="1234567890"')
        self.assertContains(response, 'value="juan@gmail.com"')
        self.assertContains(response, 'Hola, estoy interesado en tu propiedad')
    