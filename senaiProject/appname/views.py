from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User

def send_password_reset_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(smart_bytes(user.pk))

            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uid, token]))

            subject = 'Password Reset Request'
            message = f'Click on the link to reset your password: {reset_link}'
            from_email = 'tradeagile@dev.com'
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            # Pass success message to the template
            return render(request, 'forgot.html', {'email': email, 'success_message': 'E-mail enviado com sucesso!'})

        except User.DoesNotExist:
            # Pass error message to the template
            return render(request, 'forgot.html', {'error_message': 'Usuário não encontrado com esse email!'})

    else:
        return render(request, 'forgot.html')


def reset_password(request):
    return render(request, 'reset_password.html')

@csrf_exempt
def sign(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user already exists
        if User.objects.filter(username=name).exists():
            return render(request, 'sign.html', {'error_message': 'Já existe um usuário com esse username'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'sign.html', {'error_message': 'Já existe um usuário com esse e-mail.'})
        
        # Create new user
        try:
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            return render(request, 'sign.html', {'success_message': 'Usuário criado com sucesso!'})
        except Exception as e:
            return render(request, 'sign.html', {'error_message': f'Erro ao criar usuário: {str(e)}'})

    # Handle GET request
    return render(request, 'sign.html')

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error_message': 'E-mail ou senha incorretos!'})

        user = authenticate(username=user.username, password=password)

        if user:
            login_django(request, user)
            return render(request, 'login.html', {'success_message': 'Login realizado com sucesso!'})
        else:
            return render(request, 'login.html', {'error_message': 'E-mail ou senha incorretos!'})


@login_required(login_url='login')
def plataforma(request):
    return HttpResponse('Site apenas para usuários autenticados.')

@csrf_exempt
def forgot_password(request):
    return render(request, 'forgot.html')

@csrf_exempt
def inicio(request):
    return render(request, 'index.html')

def galeria_produtos(request):
    return render(request, 'produto.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Venda, ItensVenda, Cliente, Fornecedor, Vendedor
from .forms import ClienteForm
import uuid
from datetime import date
import io
from django.http import FileResponse
from django.views.generic import View
from django.db import transaction
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ClienteForm

@user_passes_test(lambda u: u.is_staff, login_url='login')
def cadastro_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ClienteForm()
    return render(request, 'cadastro_clientes.html', {'form': form})

def demonstrativo_tabelas(request):
    clientes = Cliente.objects.all()
    fornecedores = Fornecedor.objects.all()
    produtos = Produto.objects.all()
    vendas = Venda.objects.all()
    return render(request, 'demonstrativo_tabelas.html', {
        'clientes': clientes,
        'fornecedores': fornecedores,
        'produtos': produtos,
        'vendas': vendas,
    })


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from datetime import date
import uuid
from .models import Cliente, Produto, Vendedor, Venda, ItensVenda

@user_passes_test(lambda u: u.is_staff, login_url='login')
def realizar_venda(request):
    if request.method == 'POST':
        with transaction.atomic():
            cliente_id = request.POST.get('cliente')
            produto_id = request.POST.get('produto')
            quantidade = request.POST.get('quantidade')
            cliente = Cliente.objects.get(idcli=cliente_id)
            produto = Produto.objects.get(idprod=produto_id)
            vendedor = Vendedor.objects.first()  # Supondo que há um vendedor padrão
            fornecedor = produto.idforn

            quantidade = int(quantidade)
            if produto.qntdprod < quantidade:
                messages.error(request, "Estoque insuficiente para o produto.")
                clientes = Cliente.objects.all()
                produtos = Produto.objects.all()
                return render(request, 'realizar_venda.html', {
                    'clientes': clientes,
                    'produtos': produtos,
                })

            valor_venda = produto.valorprod * int(quantidade)
            codivend = uuid.uuid4().hex[:10]
            venda = Venda.objects.create(
                codivend=codivend,
                idcli=cliente,
                idforn=fornecedor,
                idvende=vendedor,
                valorvend=valor_venda,
                totalvend=valor_venda,
                datavend=date.today(),
                valorcomissao=valor_venda * vendedor.porcvende / 100
            )

            ItensVenda.objects.create(
                idvend=venda,
                idprod=produto,
                valoritvend=produto.valorprod,
                qtditvend=quantidade,
                descitvend=0
            )

            produto.qntdprod -= quantidade
            produto.save()

            return redirect('inicio')

    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'realizar_venda.html', {
        'clientes': clientes,
        'produtos': produtos,
    })



def contact_update(request, pk):
    contact = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('demonstrativo_tabelas')
    else:
        form = ClienteForm(instance=contact)
    return render(request, 'confirmar_update.html', {"form": form})

def contact_delete(request, pk):
    contact = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('demonstrativo_tabelas')
    return render(request, 'confirmar_delete.html', {'contact': contact})