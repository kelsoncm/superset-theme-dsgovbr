.. Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

Guia de Desenvolvimento
=======================

Este documento orienta desenvolvedores interessados em estender e customizar o **SupersetBR**.

Estrutura de Desenvolvimento
-----------------------------

Para iniciar o desenvolvimento do tema ou configurações adicionais:

1. **Ative o ambiente local:**
   Execute o ambiente usando o Docker Compose para desenvolvimento.
2. **Ciclo de Feedback Rápido:**
   No arquivo :file:`docker/docker-compose.yml`, o arquivo de configuração e as pastas de tema são mapeados como volumes para o container. Qualquer alteração nos arquivos locais do tema ou config será refletida instantaneamente sem necessidade de rebuildar a imagem.

Modificando o Tema DSGovBR
--------------------------

O estilo visual é controlado pelo arquivo :file:`theme/css/dsgovbr-theme.css`.

* **Customização de Cores e Fontes:** Altere os tokens CSS contidos no seletor ``:root``.
* **Componentes FAB:** Para alterar a estilização das tabelas de administração, inputs e botões padrão do Flask-AppBuilder, insira as regras específicas abaixo das variáveis.
* **Branding do Superset:** Caso precise ajustar o comportamento de cores internas do dashboard (React), edite o bloco ``THEME_OVERRIDES`` no arquivo :file:`config/superset_config.py`.

Customizando Templates do Flask-AppBuilder (FAB)
------------------------------------------------

Templates Flask localizados em :file:`theme/templates/appbuilder/` são copiados para a pasta de templates interna do Superset.

* **Layout Base:** O arquivo :file:`appbuilder/baselayout.html` injeta links de estilo e bibliotecas CSS de terceiros aplicadas de forma global.
* **Tela de Login:** O arquivo :file:`appbuilder/general/security/login_db.html` customiza os elementos, logo gov.br e formulário de acesso local.

Fluxo de Build e CI/CD
----------------------

O pipeline do GitHub Actions valida e publica as imagens de acordo com o padrão de tags Git:

1. **Tag de Desenvolvimento (Dev):**
   Tags terminadas em ``-dev`` (ex: ``v1.0.0-dev``) disparam o build e publicam a imagem no Container Registry com a tag correspondente e a tag móvel ``dev-latest``.
2. **Tag de Produção (Prod):**
   Tags puramente numéricas e sem sufixo (ex: ``v1.0.0``) disparam o build e publicam a imagem estável rotulada como ``latest``.

Ao realizar modificações no tema, certifique-se de atualizar a matriz de compatibilidade em :file:`docs/compatibility-matrix.md`.
