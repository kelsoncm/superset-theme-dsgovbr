.. Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

Dúvidas Frequentes (FAQ)
========================

Esta seção compila as principais dúvidas e resoluções de problemas comuns relacionados ao **SupersetBR**.

Como resolver erro de Iframe Bloqueado ("Refused to display... in a frame")?
---------------------------------------------------------------------------

Este erro geralmente ocorre devido a restrições do cabeçalho de segurança ``Content-Security-Policy (CSP)`` ou ``X-Frame-Options``.

1. **No Proxy Reverso (Nginx):** Certifique-se de que a diretiva ``frame-ancestors`` na CSP (localizada no arquivo :file:`infra/proxy/nginx/conf.d/default.conf`) inclua explicitamente a URL completa do portal onde o iframe está embutido.
2. **No Superset Config:** No arquivo :file:`config/superset_config.py`, certifique-se de que a diretiva ``frame_options`` no ``TALISMAN_CONFIG`` esteja definida como ``"ALLOWFROM"`` caso precise dar suporte a navegadores antigos, ou configure ``TALISMAN_ENABLED=False`` se preferir gerenciar toda a segurança de frames diretamente no Nginx.

Como atualizar o SupersetBR com a última versão do Apache Superset?
--------------------------------------------------------------------

Graças à estratégia de overrides baseada em camadas não invasivas, a atualização é simples:

1. Identifique a versão do Superset homologada que deseja utilizar.
2. No arquivo :file:`docker/Dockerfile`, atualize o valor padrão da variável ``SUPERSET_VERSION`` (ex: ``ARG SUPERSET_VERSION=4.1.0``).
3. No arquivo :file:`docs/compatibility-matrix.md`, adicione a nova linha indicando que a versão atual do tema foi validada para a nova versão do Apache Superset.
4. Execute o build local para testar a imagem:
   
   .. code-block:: bash

      docker compose -f docker/docker-compose.yml build --no-cache

O botão de login com o gov.br não aparece na tela de login
---------------------------------------------------------

O botão do gov.br só é renderizado dinamicamente pelo Flask-AppBuilder caso as configurações de autenticação do provedor OAuth2 estejam ativas.

1. Garanta que a variável de ambiente ``AUTH_TYPE`` esteja configurada com o valor ``2`` (AUTH_OAUTH).
2. Verifique se as variáveis ``OAUTH_CLIENT_ID`` e ``OAUTH_CLIENT_SECRET`` foram fornecidas e não estão vazias no arquivo de ambiente do container.
