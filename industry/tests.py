
# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class UrlTestCase(TestCase):
    def test_urls(self):
        app_name = 'industry'

        url_names = [
            'industry_list',
            'create_industry',
            'edit_industry',
        ]

        for url_name in url_names:
            try:
                if url_name == 'edit_industry':
                    company_id = 1  # Replace with a valid company ID
                    url = reverse(f'{app_name}:{url_name}', args=[company_id])
                else:
                    url = reverse(f'{app_name}:{url_name}')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
            except NoReverseMatch:
                self.fail(
                    f"URL with name '{url_name}' not found or not reversible.")


class ViewTestCase(TestCase):
    def test_industry_list(self):
        url = reverse('industry:industry_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"List of industries")

    def test_create_industry(self):
        url = reverse('industry:create_industry')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Create industry")

    def test_edit_industry(self):
        industry_id = "example-company-id"
        url = reverse('industry:edit_industry', args=[industry_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Edit or delete a industry")
