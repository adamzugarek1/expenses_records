from django.test import TestCase
from django.urls import reverse

class PageTestCase(TestCase):
    def test_display_index(self):
        response = self.client
