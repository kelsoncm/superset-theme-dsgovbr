.. Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

Integração de Embeds em Django
==============================

Este documento fornece as instruções para integrar dashboards do **SupersetBR** dentro de um portal web baseado no framework **Django** de forma autenticada e segura.

Arquitetura do Fluxo
---------------------

A integração utiliza o mecanismo de **Guest Token** (Token de Visitante) do Superset, que garante o acesso a um dashboard específico sem exigir login direto do usuário final na plataforma do Superset.

.. code-block:: text

   +----------------+           +---------------+           +---------------+
   | Navegador (F/E)|           | Django Portal |           |  SupersetBR   |
   +----------------+           +---------------+           +---------------+
           |                            |                           |
           |-- 1. Acessa Dashboard ---->|                           |
           |                            |-- 2. Login Admin JWT ---->|
           |                            |<-- 3. Retorna JWT Token --|
           |                            |                           |
           |                            |-- 4. Pede Guest Token --->|
           |                            |<-- 5. Retorna Guest Token-|
           |<-- 6. Envia Guest Token ---|                           |
           |                                                        |
           |-- 7. Inicializa SDK com Guest Token ------------------>|
           |<-- 8. Renderiza Dashboard no Iframe -------------------|

Passo 1: Implementação no Backend Django
----------------------------------------

No seu arquivo :file:`views.py` do Django (veja o exemplo completo em :file:`embeds/django/views.py`), implemente a obtenção do token JWT administrativo e a geração subsequente do Guest Token:

.. code-block:: python

   import requests
   from django.http import JsonResponse
   from django.shortcuts import render

   SUPERSET_URL = "http://localhost:8088"

   def get_guest_token(request, dashboard_id):
       # Garantir que apenas usuários autenticados no Django tenham acesso
       if not request.user.is_authenticated:
           return JsonResponse({"error": "Não autorizado"}, status=401)

       # Obter token de admin do Superset
       login_res = requests.post(f"{SUPERSET_URL}/api/v1/security/login", json={
           "username": "admin",
           "password": "admin",
           "provider": "db"
       })
       access_token = login_res.json().get("access_token")

       # Gerar Guest Token para o dashboard
       headers = {"Authorization": f"Bearer {access_token}"}
       payload = {
           "user": {
               "username": request.user.username,
               "first_name": request.user.first_name,
               "last_name": request.user.last_name
           },
           "resources": [{"type": "dashboard", "id": dashboard_id}],
           "rls": []
       }
       
       guest_res = requests.post(f"{SUPERSET_URL}/api/v1/security/guest_token/", json=payload, headers=headers)
       return JsonResponse({"token": guest_res.json().get("token")})

Passo 2: Implementação no Frontend (HTML/JS)
--------------------------------------------

No seu template Django (veja o exemplo em :file:`embeds/django/dashboard.html`), insira a div do contêiner e carregue o SDK oficial do Superset para embutir o dashboard:

.. code-block:: html

   <!-- Carregar SDK oficial -->
   <script src="https://unpkg.com/@superset-ui/embedded-sdk"></script>

   <div id="dashboard-container" style="width: 100%; height: 600px;"></div>

   <script>
       async function renderDashboard() {
           const dashboardId = "UUID_DO_SEU_DASHBOARD";
           
           // Buscar o token do backend
           const response = await fetch(`/embed/get-token/${dashboardId}/`);
           const data = await response.json();
           
           // Montar o SDK do Superset
           supersetEmbeddedSdk.embedDashboard({
               id: dashboardId,
               supersetDomain: "http://localhost:8088",
               mountPoint: document.getElementById("dashboard-container"),
               fetchGuestToken: () => data.token,
               dashboardUiConfig: {
                   hideTitle: true,
                   hideChartControls: true
               }
           });
       }
       window.onload = renderDashboard;
   </script>
