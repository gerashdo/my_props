from django.test import TestCase
from properties.forms import ContactForm

class TestForms(TestCase):

    def setUp(self):
        self.data = {
            'name': 'Juan Gonzales',
            'phone': '1234567890',
            'email': 'juan@gmail.com',
            'message': 'Hola, estoy interesado en tu propiedad'
        }

# tests for contact request form
    def test_contact_request_valid_form(self):
        form = ContactForm(self.data)
        self.assertTrue(form.is_valid())
    
    def test_contact_request_invalid_email(self):
        self.data['email'] = 'juan@gmail'
        form = ContactForm(self.data)
        self.assertFalse(form.is_valid())
    
    def test_contact_request_phone_should_be_10_long(self):
        self.data['phone'] = '12345678'
        form = ContactForm(self.data)
        self.assertFalse(form.is_valid())
        self.data['phone'] = '12345678901'
        form = ContactForm(self.data)
        self.assertFalse(form.is_valid())

    def test_contact_request_phone_should_be_just_numbers(self):
        self.data['phone'] = '123456789a'
        form = ContactForm(self.data)
        self.assertFalse(form.is_valid())

    def test_contact_request_name_should_be_at_least_6_characters(self):
        self.data['name'] = 'Juan'
        form = ContactForm(self.data)
        self.assertFalse(form.is_valid())

    def test_contact_request_message_should_be_at_least_10_characters(self):
        self.data['message'] = 'interesa'
        form = ContactForm(self.data)
        self.assertFalse(form.is_valid())


    

    
