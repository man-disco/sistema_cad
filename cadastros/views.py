from django.shortcuts import render, reverse, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from .models import Cadastro
from .forms import NovoCadastro


# Create your views here.
@login_required(login_url='login')
def index(request):
    """Mostra a página inicial com a data atual."""
    data_atual = timezone.now()
    context = {'data_atual': data_atual}
    return render(request, "dados/index.html", context)


@login_required(login_url='login')
@permission_required('cadastros.view_cadastro', raise_exception=True)
def cadastros(request):
    """Mostra todos os cadastros existentes e os retorna ao usuário."""

    cadastros = Cadastro.objects.all()
    paginas = Paginator(cadastros, 10)
    num_pagina = request.GET.get("pagina")
    obj_pagina = paginas.get_page(num_pagina)
    context = {"cadastros": cadastros, "obj_pagina": obj_pagina}
    return render(request, "dados/cadastros.html", context)


@login_required(login_url='login')
# Se o usuário não tiver a permissão para adicionar (ou visualizar) cadastros, a página retorna um erro 403.
@permission_required('cadastros.add_cadastro', raise_exception=True)
def criar_cadastro(request):
    """Cria um novo registro no banco de dados."""

    # Cria um novo formulário e salva os dados inseridos nele (caso a requisição seja POST).
    # Se a requisição for um GET, mostra o formulário em branco.
    if request.method == "POST":
        form = NovoCadastro(request.POST)
        # Verifica se os dados informados são válidos, se forem, salva o formulário.
        if form.is_valid():
            cadastro = form.save(commit=False)
            cadastro.save()
            return HttpResponseRedirect(reverse('cadastros'))
    else:
        form = NovoCadastro()
    context = {"form": form}
    return render(request, "dados/criar_cadastro.html", context)


# Se o usuário não tiver a permissão para adicionar (ou visualizar) cadastros, a página retorna um erro 403.
@permission_required('cadastros.change_cadastro', raise_exception=True)
def editar_cadastro(request, cadastro_id):
    """Edita um cadastro existente."""

    # Verifica se o ID do cadastro a ser editado é válido, se não for, mostra um erro 404.
    cadastro = get_object_or_404(Cadastro, pk=cadastro_id)
    if request.method == "POST":
        form = NovoCadastro(instance=cadastro, data=request.POST)
        # Verifica se os dados informados são válidos, se forem, salva o formulário.
        if form.is_valid():
            cadastro.alterado_por = request.user
            form.save()
            return HttpResponseRedirect(reverse('cadastros'))
    else:
        form = NovoCadastro(instance=cadastro)
    context = {"form": form, 'cadastro': cadastro}
    return render(request, "dados/editar_cadastro.html", context)


@login_required(login_url='login')
# Se o usuário não tiver a permissão para deletar cadastros, a página retorna um erro 403.
@permission_required('cadastros.delete_cadastro', raise_exception=True)
def deletar_cadastro(request, cadastro_id):
    """Deleta um registro no banco de dados."""
    
    # Verifica se o ID do cadastro a ser editado é válido, se não for, mostra um erro 404.
    cadastro = get_object_or_404(Cadastro, pk=cadastro_id)
    if request.method == 'POST' and 'deletar' in request.POST:
        cadastro.delete()
        return HttpResponseRedirect(reverse('cadastros'))

    context = {'cadastro': cadastro}
    return render(request, "dados/deletar_cadastro.html", context)


@login_required(login_url='login')
@permission_required('cadastros.view_cadastro')
def resultado_pesquisa(request):
    """Busca um cadastro especifico no sistema."""
    filtro = request.GET.get("filtro")
    pesquisa = request.GET.get("query")


    # Cria filtros com base na seleção do usuário e retorna os resultados correspondentes.
    if filtro == "ID":
        try:
            resultado = Cadastro.objects.filter(id=pesquisa)
        except ValueError:
            # Se o valor de resultado com o filtro de ID for ínvalido, a variável resultado não é definida com um valor.
            resultado = None
    if filtro == "Nome":
        resultado = Cadastro.objects.filter(Q(nome__icontains=pesquisa))
    if filtro == "Endereço":
        resultado = Cadastro.objects.filter(Q(endereço__icontains=pesquisa))

    context = {'filtro': filtro, 'pesquisa': pesquisa, 'resultado': resultado}
    return render(request, "dados/resultado_busca.html", context)


def acesso_negado_usuario(request, exception):
    response = render(request, 'dados/403.html', {'exception': exception})
    response.status_code = 403
    return response
