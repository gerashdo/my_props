from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
   
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
        self.assertNotContains(response, 'Next page')

    def test_first_properties_page_shoul_have_next_page_link(self):
        response = self.client.get('/')
        self.assertContains(response, 'Next page')
    
    def test_first_properties_page_should_have_15_image_tags(self):
        response = self.client.get('/')
        self.assertContains(response, '<img src="', count=15)