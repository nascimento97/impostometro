"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do schema do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Impostômetro API",
        default_version='v1',
        description="""
        API para gerenciamento de despesas, ingredientes, produtos e análise financeira.
        
        ## Funcionalidades principais:
        - **Usuários**: Gerenciamento de usuários e autenticação
        - **Despesas Fixas**: Controle de despesas fixas mensais
        - **Despesas Variáveis**: Controle de despesas variáveis
        - **Ingredientes**: Cadastro e gerenciamento de ingredientes
        - **Produtos**: Cadastro e gerenciamento de produtos
        - **Análise Financeira**: Relatórios e análises financeiras
        
        ## Autenticação:
        Esta API utiliza autenticação JWT (JSON Web Token). Para acessar os endpoints protegidos:
        1. Faça login através do endpoint `/api/auth/login/`
        2. Use o token retornado no header Authorization: `Bearer {seu_token}`
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@impostometro.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Apps
    path('', include('usuarios.urls')),
    path('', include('despesafixa.urls')),
    path('', include('despesavariavel.urls')),
    path('', include('ingredientes.urls')),
    path('', include('produtos.urls')),
    path('', include('analisefinanceira.urls')),
    
    # JWT Authentication endpoints (alternativa aos endpoints customizados)
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# URLs do Swagger - apenas em desenvolvimento
if settings.DEBUG:
    urlpatterns += [
        # Swagger UI
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        
        # ReDoc UI (alternativa ao Swagger UI)
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        
        # Schema JSON (para download)
        path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema'),
    ]
