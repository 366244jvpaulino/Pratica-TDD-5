from django.urls import path
from core.views import (
    login,
    logout,
    home,
    list_links,
    create_link,
    edit_link,
    delete_link,
)


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('', home, name='home'),
    path('links/', list_links, name='link_list'),
    path('links/novo/', create_link, name='link_create'),
    path('links/<int:pk>/editar/', edit_link, name='link_edit'),
    path('links/<int:pk>/excluir/', delete_link, name='link_delete'),
]