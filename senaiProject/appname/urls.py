from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import contact_delete, contact_update

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cadastro_clientes/', views.cadastro_clientes, name='cadastro_clientes'),
    path('demonstrativo_tabelas/', views.demonstrativo_tabelas, name='demonstrativo_tabelas'),
    path('galeria_produtos/', views.galeria_produtos, name='galeria_produtos'),
    path('realizar_venda/', views.realizar_venda, name='realizar_venda'),
    path('contact_delete/<int:pk>/', contact_delete, name='contact_delete'),
    path('contact_update/<int:pk>/', contact_update, name='contact_update'),
    path('sign/', views.sign, name='sign'),
    path('login/', views.login, name='login'),
    
    # URL para enviar e-mail de recuperação de senha
    path('forgot_password/', views.send_password_reset_email, name='forgot_password'),

    # URL para redefinição de senha
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # URLs adicionais do fluxo de redefinição de senha, se necessário
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
