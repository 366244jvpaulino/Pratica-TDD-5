from django.shortcuts import render, redirect, get_object_or_404
from core.forms import LoginForm, LinkModelForm
from core.models import LinkModel
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': LoginForm()})


def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    return render(request, 'index.html')


@login_required
def list_links(request):
    links = LinkModel.objects.all()
    return render(request, 'links/list.html', {'links': links})


@login_required
def create_link(request):
    if request.method == "POST":
        form = LinkModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('link_list')
    else:
        form = LinkModelForm()
    return render(request, 'links/form.html', {'form': form, 'title': 'Cadastrar Link'})


@login_required
def edit_link(request, pk):
    link = get_object_or_404(LinkModel, pk=pk)
    if request.method == "POST":
        form = LinkModelForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('link_list')
    else:
        form = LinkModelForm(instance=link)
    return render(request, 'links/form.html', {'form': form, 'title': 'Editar Link'})


@login_required
def delete_link(request, pk):
    link = get_object_or_404(LinkModel, pk=pk)
    if request.method == "POST":
        link.delete()
        return redirect('link_list')
    return render(request, 'links/confirm_delete.html', {'link': link})
