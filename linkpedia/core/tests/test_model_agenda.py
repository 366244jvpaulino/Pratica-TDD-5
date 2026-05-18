from django.test import TestCase
from core.models import LinkModel


class LinkModelTest(TestCase):

    def setUp(self):
        self.link = LinkModel.objects.create(
            titulo="OpenAI",
            link="https://openai.com",
            observacao="Site oficial da OpenAI."
        )

    def test_link_criado_com_sucesso(self):
        self.assertEqual(self.link.titulo, "OpenAI")
        self.assertEqual(self.link.link, "https://openai.com")
        self.assertEqual(
            self.link.observacao,
            "Site oficial da OpenAI."
        )

    def test_str_retorna_titulo_e_link(self):
        self.assertEqual(
            str(self.link),
            "OpenAI - https://openai.com"
        )