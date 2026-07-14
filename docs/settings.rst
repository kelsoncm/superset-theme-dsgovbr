.. Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

Configurações e Variáveis de Ambiente
=====================================

O comportamento do **SupersetBR** é inteiramente configurável através de variáveis de ambiente passadas ao container. A lógica de leitura destas variáveis reside no arquivo :file:`config/superset_config.py`.

Variáveis de Infraestrutura
----------------------------

.. list-table::
   :widths: 30 40 30
   :header-rows: 1

   * - Variável
     - Descrição
     - Valor Padrão
   * - ``SUPERSET_SECRET_KEY``
     - Chave secreta de criptografia da sessão Flask (Obrigatória em Produção).
     - ``um_segredo_muito_longo_e_aleatorio_12345``
   * - ``SQLALCHEMY_DATABASE_URI``
     - String de conexão com o banco de metadados PostgreSQL.
     - ``postgresql://superset:superset_password@db:5432/superset``
   * - ``REDIS_HOST``
     - Host do serviço de cache Valkey/Redis.
     - ``valkey``
   * - ``REDIS_PORT``
     - Porta do serviço de cache Valkey/Redis.
     - ``6379``

Configurações de Autenticação
-----------------------------

A autenticação é definida pela variável ``AUTH_TYPE``:

* **``AUTH_TYPE=1`` (Local / AUTH_DB):** Usa o banco de usuários interno do Superset (Padrão).
* **``AUTH_TYPE=2`` (OAuth2 / AUTH_OAUTH):** Habilita provedores externos de login, como o **acesso.gov.br**.
* **``AUTH_TYPE=3`` (LDAP / AUTH_LDAP):** Autentica usuários através de um diretório LDAP/Active Directory corporativo.

Variáveis de Autenticação OAuth2 (acesso.gov.br)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se ``AUTH_TYPE=2``, as seguintes variáveis devem ser informadas:

.. list-table::
   :widths: 30 40 30
   :header-rows: 1

   * - Variável
     - Descrição
     - Exemplo / Padrão
   * - ``OAUTH_CLIENT_ID``
     - ID do cliente fornecido pelo cadastro no acesso.gov.br.
     - ``meu-client-id``
   * - ``OAUTH_CLIENT_SECRET``
     - Segredo do cliente fornecido pelo cadastro no acesso.gov.br.
     - ``segredo-oauth-123``
   * - ``OAUTH_API_BASE_URL``
     - URL base da API do Provedor de Identidade do Governo.
     - ``https://sso.staging.acesso.gov.br/``

Variáveis de Autenticação LDAP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se ``AUTH_TYPE=3``:

.. list-table::
   :widths: 30 40 30
   :header-rows: 1

   * - Variável
     - Descrição
     - Exemplo / Padrão
   * - ``AUTH_LDAP_SERVER``
     - Endereço do servidor LDAP.
     - ``ldap://ldap.meuorgao.gov.br:389``
   * - ``AUTH_LDAP_USE_TLS``
     - Habilitar conexão segura TLS com o LDAP (True/False).
     - ``True``
   * - ``AUTH_LDAP_SEARCH``
     - Base de busca DN para localização de usuários.
     - ``ou=usuarios,dc=meuorgao,dc=gov,dc=br``
   * - ``AUTH_LDAP_UID_KEY``
     - Atributo identificador do usuário no diretório.
     - ``uid`` ou ``sAMAccountName``
