<?php
/**
 * Exemplo de código PHP para uso em um bloco ou página customizada no Moodle.
 * Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.
 */

defined('MOODLE_INTERNAL') || die();

class block_superset_embed extends block_base {
    
    public function init() {
        $this->title = get_string('pluginname', 'block_superset_embed');
    }

    public function get_content() {
        global $USER, $PAGE;

        if ($this->content !== null) {
            return $this->content;
        }

        $this->content = new stdClass();
        
        // 1. Validar se o usuário está autenticado no Moodle (Auth no host)
        if (!isloggedin() || isguestuser()) {
            $this->content->text = get_string('not_authorized', 'block_superset_embed');
            return $this->content;
        }

        // Configurações do SupersetBR
        $superset_url = 'http://localhost:8088';
        $admin_username = 'admin';
        $admin_password = 'admin';
        $dashboard_uuid = 'INSERIR_UUID_DO_DASHBOARD'; // O UUID do dashboard a ser exibido

        // 2. Obter Token Administrativo via cURL no backend
        $token = $this->get_superset_token($superset_url, $admin_username, $admin_password);
        if (!$token) {
            $this->content->text = 'Erro ao autenticar no serviço de relatórios.';
            return $this->content;
        }

        // 3. Obter Guest Token para o usuário atual do Moodle
        $guest_token = $this->get_guest_token($superset_url, $token, $dashboard_uuid, $USER);
        if (!$guest_token) {
            $this->content->text = 'Erro ao gerar credenciais de acesso ao relatório.';
            return $this->content;
        }

        // 4. Montar a exibição com o script SDK do Superset
        // Adiciona o SDK do Superset na página do Moodle
        $PAGE->requires->js_by_url('https://unpkg.com/@superset-ui/embedded-sdk');

        $html = '
        <div id="superset-moodle-container" style="width: 100%; height: 500px; border: 1px solid #ddd; background: #fff;"></div>
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                if (typeof supersetEmbeddedSdk !== "undefined") {
                    supersetEmbeddedSdk.embedDashboard({
                        id: "' . $dashboard_uuid . '",
                        supersetDomain: "' . $superset_url . '",
                        mountPoint: document.getElementById("superset-moodle-container"),
                        fetchGuestToken: () => "' . $guest_token . '",
                        dashboardUiConfig: {
                            hideTitle: true,
                            hideTabParent: true,
                            hideChartControls: true
                        }
                    });
                } else {
                    console.error("SDK do Superset não foi carregado corretamente.");
                }
            });
        </script>';

        $this->content->text = $html;
        return $this->content;
    }

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
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        
        $result = curl_exec($ch);
        $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpcode === 200) {
            $data = json_decode($result, true);
            return $data['access_token'] ?? null;
        }
        return null;
    }

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
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);

        $result = curl_exec($ch);
        $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpcode === 200) {
            $data = json_decode($result, true);
            return $data['token'] ?? null;
        }
        return null;
    }
}
