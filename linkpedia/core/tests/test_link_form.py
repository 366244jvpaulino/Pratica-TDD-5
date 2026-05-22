from django.test import TestCase
from core.forms import LinkModelForm


class LinkModelFormTest(TestCase):

    def test_form_has_fields(self):
        form = LinkModelForm()
        expected = ['titulo', 'link', 'observacao']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_form_valid_data(self):
        form = LinkModelForm(data={
            'titulo': 'OpenAI',
            'link': 'https://openai.com',
            'observacao': 'Site oficial da OpenAI.',
        })
        self.assertTrue(form.is_valid())

    def test_form_rejects_invalid_url(self):
        form = LinkModelForm(data={
            'titulo': 'OpenAI',
            'link': 'not-a-url',
            'observacao': 'Teste',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('link', form.errors)
