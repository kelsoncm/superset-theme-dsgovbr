.. Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

Integração de Embeds no Moodle
=============================

Este documento detalha o processo de integração de dashboards do **SupersetBR** em ambientes virtuais de aprendizagem baseados no **Moodle**.

Estratégia de Integração
------------------------

A integração no Moodle é implementada através da criação de um Bloco customizado (Block Plugin) ou carregando código PHP direto em uma página. O backend em PHP do Moodle realiza chamadas seguras via cURL para obter o Guest Token do Superset e renderiza o script com o SDK do lado do cliente.

Implementação do Bloco PHP do Moodle
------------------------------------

No arquivo do seu plugin (ex: :file:`block_superset_embed.php` ou similar, detalhado em :file:`embeds/moodle/embed_block.php`), implemente as chamadas seguras cURL para autenticação e geração de token:

.. code-block:: php

   <?php
   // Autenticação administrativa no Superset
   private function get_superset_token($url, $username, $password) {
       $ch = curl_init($url . '/api/v1/security/login');
       $payload = json_encode([
           'username' => $username,
           'password' => $password,
           'provider' => 'db'
       ]);
       curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
       curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type:application/json']);
       curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
       $result = curl_exec($ch);
       $data = json_decode($result, true);
       return $data['access_token'] ?? null;
   }

   // Geração do token temporário para o usuário logado no Moodle
   private function get_guest_token($url, $admin_token, $dashboard_uuid, $user) {
       $ch = curl_init($url . '/api/v1/security/guest_token/');
       $payload = json_encode([
           'user' => [
               'username' => $user->username,
               'first_name' => $user->firstname,
               'last_name' => $user->lastname
           ],
           'resources' => [
               ['type' => 'dashboard', 'id' => $dashboard_uuid]
           ],
           'rls' => []
       ]);
       curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
       curl_setopt($ch, CURLOPT_HTTPHEADER, [
           'Content-Type:application/json',
           'Authorization: Bearer ' . $admin_token
       ]);
       curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
       $result = curl_exec($ch);
       $data = json_decode($result, true);
       return $data['token'] ?? null;
   }

Renderização do Bloco no Navegador
-----------------------------------

O Moodle injeta o SDK do Superset e o script JS para inicializar o contêiner. Certifique-se de carregar o SDK em seu tema ou diretamente na estrutura de script do bloco:

.. code-block:: php

   <?php
   // Adiciona o script SDK ao cabeçalho da página do Moodle
   $PAGE->requires->js_by_url('https://unpkg.com/@superset-ui/embedded-sdk');

   // Container HTML + JS de inicialização
   $html = '
   <div id="superset-moodle-container" style="width:100%; height:500px; border:1px solid #ccc;"></div>
   <script>
       document.addEventListener("DOMContentLoaded", function() {
           supersetEmbeddedSdk.embedDashboard({
               id: "' . $dashboard_uuid . '",
               supersetDomain: "' . $superset_url . '",
               mountPoint: document.getElementById("superset-moodle-container"),
               fetchGuestToken: () => "' . $guest_token . '",
               dashboardUiConfig: {
                   hideTitle: true,
                   hideTabParent: true
               }
           });
       });
   </script>';

Considerações de Segurança
--------------------------

* **Domínios Permitidos (CSP):** Certifique-se de que a configuração do Nginx no proxy reverso do SupersetBR permita o domínio do Moodle na diretiva ``frame-ancestors`` (dentro do cabeçalho ``Content-Security-Policy``).
* **Nível de Permissão:** Recomenda-se criar um usuário com perfil mínimo no Superset apenas para requisição de tokens (e.g. papel Gamma/público) a fim de restringir o escopo em caso de vazamento de chaves.
* **Comunicação Segura:** Use HTTPS em produção em toda a comunicação entre o Moodle e o Superset.
