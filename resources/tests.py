from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from .models import Data


# Create your tests here.

class TestViews(TestCase):

    def test_upload_csv_POST(self):
        c = Client()
        import os
        module_dir = os.path.dirname(__file__)  # get current directory

        file_path = os.path.join(module_dir, 'dummy_data')
        with open(file_path) as tsf:
            c.post('admin/resources/data/add_from_file/', {'FILES': [tsf]})
        response = c.get(reverse(''))
        self.assertEquals(response.status_code, 200)