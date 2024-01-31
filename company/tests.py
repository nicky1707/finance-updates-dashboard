from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class UrlTestCase(TestCase):
    def test_urls(self):
        app_name = 'company'

        url_names = [
            'company_list',
            'create_company',
            'edit_company',
        ]

        for url_name in url_names:
            try:
                if url_name == 'edit_company':
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
    def test_company_list(self):
        url = reverse('company:company_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"List of companies")

    def test_create_company(self):
        url = reverse('company:create_company')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"create a company")

    def test_edit_company(self):
        company_id = "example-company-id"
        url = reverse('company:edit_company', args=[company_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Edit or delete a company")
