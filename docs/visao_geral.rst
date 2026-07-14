.. Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

Visão Geral do SupersetBR
=========================

O **SupersetBR** visa preencher a lacuna de soluções de Analytics e Business Intelligence corporativas no setor público brasileiro que necessitam de forte aderência visual ao **Design System do Governo Federal (DSGovBR)**.

Objetivo do Projeto
-------------------

O principal objetivo deste projeto é disponibilizar um pacote pronto e conteinerizado do Apache Superset, contendo uma estratégia de customização visual que reflita as cores, espaçamentos, tipografia e acessibilidade oficiais do portal **gov.br**, mantendo a compatibilidade direta com a ramificação oficial do Apache Superset (upstream).

Pilares do Projeto
------------------

1. **Design System First:** O tema e a identidade visual devem ser 100% aderentes às especificações do DSGovBR.
2. **Upstream-first (Sem fork por padrão):** Priorizar overrides em camadas externas suportadas (Python config, CSS injetado e templates do FAB) antes de realizar patches na aplicação React. Isso minimiza a carga de trabalho em atualizações de versão do Apache Superset.
3. **Configuração como Código:** Todas as parametrizações de infraestrutura, autenticação e visual devem ser rastreáveis via Git e configuráveis por variáveis de ambiente.

Pilha Tecnológica Homologada
-----------------------------

* **Core da Aplicação:** Apache Superset 4.0.2+
* **Banco de Metadados:** PostgreSQL 15+
* **Cache e Broker:** Valkey 7.2+
* **Fronteira HTTP e Cabeçalhos:** Nginx 1.25+ (Proxy Reverso)

Arquitetura de Overrides
------------------------

A identidade visual do SupersetBR é injetada nas seguintes camadas:

* **Configurações Globais:** Realizadas no arquivo `config/superset_config.py`.
* **Identidade Visual:** Concentrada na folha de estilo `theme/css/dsgovbr-theme.css`.
* **Templates da Tela de Login e Layout:** Sobrescrevem o Flask-AppBuilder dentro de `theme/templates/appbuilder/`.
