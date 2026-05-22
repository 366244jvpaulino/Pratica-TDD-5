from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.shortcuts import resolve_url as r
from http import HTTPStatus

from core.models import LinkModel


class LinksCrudTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='aluno@cps.sp.gov.br',
            password='123mudar'
        )
        self.client.login(username='admin', password='123mudar')

    def test_link_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(r('link_list'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(r('login'), response.url)

    def test_create_link(self):
        data = {
            'titulo': 'OpenAI',
            'link': 'https://openai.com',
            'observacao': 'Site oficial da OpenAI.',
        }
        response = self.client.post(r('link_create'), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(LinkModel.objects.filter(titulo='OpenAI').exists())
        self.assertTemplateUsed(response, 'links/list.html')

    def test_list_links(self):
        LinkModel.objects.create(
            titulo='OpenAI',
            link='https://openai.com',
            observacao='Site oficial da OpenAI.',
        )
        response = self.client.get(r('link_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'OpenAI')
        self.assertTemplateUsed(response, 'links/list.html')

    def test_edit_link(self):
        link = LinkModel.objects.create(
            titulo='OpenAI',
            link='https://openai.com',
            observacao='Site oficial da OpenAI.',
        )
        data = {
            'titulo': 'OpenAI Atualizado',
            'link': 'https://openai.com',
            'observacao': 'Link atualizado.',
        }
        response = self.client.post(r('link_edit', pk=link.pk), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        link.refresh_from_db()
        self.assertEqual(link.titulo, 'OpenAI Atualizado')
        self.assertTemplateUsed(response, 'links/list.html')

    def test_delete_link(self):
        link = LinkModel.objects.create(
            titulo='OpenAI',
            link='https://openai.com',
            observacao='Site oficial da OpenAI.',
        )
        response_get = self.client.get(r('link_delete', pk=link.pk))
        self.assertEqual(response_get.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response_get, 'links/confirm_delete.html')

        response_post = self.client.post(r('link_delete', pk=link.pk), follow=True)
        self.assertEqual(response_post.status_code, HTTPStatus.OK)
        self.assertFalse(LinkModel.objects.filter(pk=link.pk).exists())
        self.assertTemplateUsed(response_post, 'links/list.html')
