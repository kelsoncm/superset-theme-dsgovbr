# Exemplo de integração do SupersetBR com Django para Embed Privado
# Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

SUPERSET_URL = getattr(settings, "SUPERSET_URL", "http://localhost:8088")
SUPERSET_ADMIN_USERNAME = getattr(settings, "SUPERSET_ADMIN_USERNAME", "admin")
SUPERSET_ADMIN_PASSWORD = getattr(settings, "SUPERSET_ADMIN_PASSWORD", "admin")


def get_superset_access_token():
    """
    Autentica no Apache Superset com credenciais administrativas
    para obter o token JWT de acesso à API.
    """
    url = f"{SUPERSET_URL}/api/v1/security/login"
    payload = {
        "username": SUPERSET_ADMIN_USERNAME,
        "password": SUPERSET_ADMIN_PASSWORD,
        "provider": "db",
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json().get("access_token")


def get_guest_token(request, dashboard_id):
    """
    View Django para solicitar um Guest Token (Token de Visitante) ao Superset.
    Isso garante que o usuário autenticado no portal Django possa ver o
    dashboard sem ter que se logar novamente no Superset.
    """
    # 1. Verificar se o usuário está logado no Django (Auth principal no portal host)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Nao autorizado"}, status=401)

    try:
        # 2. Obter token de acesso administrativo do Superset
        access_token = get_superset_access_token()

        # 3. Solicitar o Guest Token para o dashboard específico
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        # Define os recursos aos quais o usuário terá acesso temporário
        payload = {
            "user": {
                "username": request.user.username,
                "first_name": request.user.first_name or request.user.username,
                "last_name": request.user.last_name or "Portal",
            },
            "resources": [{"type": "dashboard", "id": dashboard_id}],
            "rls": [],  # Adicione regras de Row Level Security se necessário
        }

        url = f"{SUPERSET_URL}/api/v1/security/guest_token/"
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        
        guest_token = response.json().get("token")
        return JsonResponse({"token": guest_token})

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Erro de comunicacao com o Superset: {str(e)}"}, status=502)


def dashboard_page(request):
    """
    Renderiza a página HTML que carrega o superset-embedded-sdk.
    """
    context = {
        "dashboard_id": "MODIFIQUE_PELO_UUID_DO_SEU_DASHBOARD",
        "superset_url": SUPERSET_URL
    }
    return render(request, "embeds/django/dashboard.html", context)
