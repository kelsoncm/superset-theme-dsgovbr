.. Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

Guia de Implantação
==================

Este guia orienta a implantação do **SupersetBR** utilizando o baseline padrão do projeto baseado em **Docker Compose** e **Nginx**.

Requisitos de Infraestrutura
----------------------------

* **Docker Engine** v20.10+
* **Docker Compose** v2.0+
* Mínimo de 4GB de memória RAM disponível na máquina servidora.
* Acesso à internet para build inicial da imagem e download de dependências upstream do Apache Superset.

Estrutura de Containers
-----------------------

A implantação padrão disponibiliza cinco contêineres atuando de forma integrada:

1. **superset_db (db):** PostgreSQL para persistência dos metadados.
2. **superset_valkey (valkey):** Valkey/Redis para cache de consultas e sessões.
3. **superset_app (superset):** Aplicação executando o core do Superset customizado.
4. **superset_init (superset-init):** Executa migrações iniciais e criação da conta de admin.
5. **superset_proxy (proxy):** Nginx como front-end HTTP/HTTPS.

Passo a Passo de Implantação
-----------------------------

1. **Definição de Variáveis de Ambiente:**
   Recomenda-se criar um arquivo :file:`.env` no diretório :file:`docker/` para armazenar as credenciais e evitar o uso de credenciais padrão em produção:

   .. code-block:: bash

      # docker/.env
      DB_PASSWORD=senha_segura_do_banco_postgresql
      ADMIN_PASSWORD=senha_segura_do_administrador
      SUPERSET_SECRET_KEY=chave_secreta_longa_gerada_aleatoriamente

2. **Inicialização do Ambiente:**
   Execute o comando a partir da raiz do repositório:

   .. code-block:: bash

      docker compose -f docker/docker-compose.yml up -d

3. **Monitoramento de Inicialização:**
   Acompanhe o processo de migração de banco executado pelo container ``superset_init``:

   .. code-block:: bash

      docker logs -f superset_init

   Assim que o container ``superset_init`` encerrar sua execução com a mensagem ``Inicializacao completa.``, o ambiente estará pronto.

Configuração do Proxy Reverso (Nginx)
--------------------------------------

A camada de proxy reverso é essencial para aplicar segurança de borda. O arquivo :file:`infra/proxy/nginx/conf.d/default.conf` já inclui regras básicas de proteção contra XSS, Clickjacking e injeções maliciosas.

Para implantações corporativas reais, recomenda-se:

* Ativar SSL/TLS (HTTPS) fornecendo certificados válidos (ex: Let's Encrypt).
* Configurar o cabeçalho ``Content-Security-Policy (CSP)`` para refletir o nome de domínio da sua instituição.
* Restringir o cabeçalho ``frame-ancestors`` na CSP para permitir apenas domínios confiáveis onde dashboards serão incorporados (embeds).
