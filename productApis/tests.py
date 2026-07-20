from pathlib import Path
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from productApis.views import addAProduct


class AddProductViewTests(TestCase):
    def test_returns_404_when_product_data_is_missing(self):
        factory = APIRequestFactory()
        request = factory.post('/addAProduct', {'asin': 'B07VXJBP8R'}, format='json')

        with patch('productApis.views.create_product_object', return_value=None):
            response = addAProduct(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 404)

    def test_logs_exception_to_file_when_product_lookup_fails(self):
        factory = APIRequestFactory()
        request = factory.post('/addAProduct', {'asin': 'B07VXJBP8R'}, format='json')
        log_path = Path(__file__).resolve().parent / 'logs' / 'product_api.log'

        if log_path.exists():
            log_path.unlink()

        with patch('productApis.views.create_product_object', side_effect=RuntimeError('boom')):
            response = addAProduct(request)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(log_path.exists())
        self.assertIn('boom', log_path.read_text(encoding='utf-8'))
