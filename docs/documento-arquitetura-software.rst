.. Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

============================================
Documento de Arquitetura de Software (DAS)
============================================

SupersetBR - Tema do Superset no padrão do Design System do Governo Federal o Brasil (DSGovBR)

Resumo executivo
================

O projeto SupersetBR - Tema do Superset no padrão do Design System do Governo Federal o Brasil (DSGovBR) tem por objetivo adaptar o Apache Superset para funcionar como solução institucional de analytics com identidade visual alinhada ao Design System do Governo Federal (DSGovBR), promovendo experiência unificada, acessível e coerente com o Padrão Digital de Governo. Trata-se de uma iniciativa open source, licenciada sob Apache-2.0, que privilegia o reuso de software público, a transparência e a sustentabilidade tecnológica no ecossistema governamental.

A arquitetura proposta adota o Apache Superset como plataforma-base de visualização de dados, operando inicialmente sobre Docker Compose, com PostgreSQL como banco de metadados, Valkey como camada de cache e reverse proxy compatível (Nginx ou Traefik) como fronteira de publicação. A solução prevê ambientes separados de desenvolvimento e produção, com automação de build e deploy por meio de GitHub Actions e política explícita de versionamento para a aplicação e para o tema institucional DSGovBR.

Do ponto de vista de identidade e experiência do usuário, o projeto busca um white-label institucional quase total, combinando configuração oficial do Superset, assets e templates próprios, além de um tema visual que materializa tokens, componentes e diretrizes do DSGovBR. A estratégia de customização é orientada por princípios upstream-first e "sem fork por padrão", privilegiando mecanismos de override em camadas estáveis (configuração Python, imagem customizada, templates e CSS institucional) e reservando modificações profundas em frontend para exceções justificadas por decisões arquiteturais formais.

A solução contempla autenticação configurável, incluindo login local do Superset, OAuth2 (com destaque para integração com o acesso.gov.br), LDAP e possibilidade de evolução futura para outros mecanismos, preservando flexibilidade para diferentes cenários institucionais. Para consumo de informações, o projeto suporta o uso da interface nativa do Superset e a publicação de embeds públicos e privados, aptos a serem incorporados em portais baseados em Django e Moodle, respeitando políticas de segurança, cache e governança de acesso definidas pela instituição.

O Documento de Arquitetura de Software correspondente detalha a arquitetura lógica e física, a matriz de componentes, os "pontos de override" por camada, os riscos arquiteturais e um checklist de upgrade que orienta a evolução controlada da solução em alinhamento com o upstream do Apache Superset. Em síntese, o SupersetBR oferece uma base robusta para construção de painéis e análises de dados em ambientes públicos, conciliando padrão visual governamental, governança de software livre e pragmatismo operacional.

Projeto
=======

**Nome temporário do projeto:** SupersetBR - Tema do Superset no padrão do Design System do Governo Federal o Brasil (DSGovBR)

Histórico de versões
====================

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Versão
     - Data
     - Descrição
   * - 0.1.0
     - 2026-07-14
     - Versão inicial do Documento de Arquitetura de Software

Objetivo
========

Este Documento de Arquitetura de Software estabelece a arquitetura de referência do projeto Superset Institucional DS-BR, iniciativa open source voltada à adaptação do Apache Superset para um cenário de white-label institucional quase total, com aderência explícita ao Design System do governo brasileiro (gov.br / DS-BR), preservando, sempre que possível, compatibilidade com o upstream e baixa carga de manutenção evolutiva. [cite:13][cite:21][cite:32]

O documento tem finalidade institucional e técnica, servindo como base para fomento, governança de desenvolvimento, implantação, sustentação, gestão de riscos e evolução da solução. O texto adota linguagem executiva-institucional nas seções de decisão e governança, mantendo detalhamento hands-on apenas nas partes necessárias para explicitar os pontos de override e sua estratégia de operação. [cite:21][cite:22][cite:26]

Escopo
======

O escopo deste DAS cobre a customização do Apache Superset para identidade institucional baseada no DS-BR, autenticação configurável, suporte a ambientes de desenvolvimento e produção, implantação inicial em Docker Compose, arquitetura futura de referência em Kubernetes, pipeline CI/CD em GitHub Actions, suporte a embeds públicos e privados, além da definição dos mecanismos de override necessários para personalização visual, funcional e operacional. [cite:21][cite:22][cite:27]

Não fazem parte do escopo deste documento a implementação detalhada do conteúdo visual definitivo, a modelagem analítica dos datasets, o catálogo completo de dashboards por área de negócio, nem a adoção inicial de autenticação JWT como mecanismo principal, a qual foi conscientemente postergada em favor da simplificação arquitetural com OAuth2 na primeira etapa. [cite:31][cite:32]

Referências arquiteturais
=========================

* Apache Superset - documentação oficial de configuração e implantação. [cite:21][cite:22][cite:27][cite:30]
* Apache Superset - práticas de customização em imagens e assets. [cite:23]
* Metabase - documentação oficial de appearance e branding. [cite:11][cite:19]
* Metabase - limitações relatadas pela comunidade para customização por CSS na edição OSS. [cite:12][cite:16]
* GOVBR-DS - portal oficial e repositórios do padrão digital de governo. [cite:26][cite:29][cite:32]

Visão executiva
===============

A arquitetura proposta adota o Apache Superset como plataforma-base de analytics e visualização, encapsulada por uma camada de configuração institucional, tema DS-BR, assets próprios, mecanismos de autenticação configuráveis e pipeline controlado de build e deploy. Essa abordagem permite atingir forte aderência visual e institucional sem assumir, como estratégia primária, um fork profundo do frontend do projeto, reduzindo custos de manutenção e riscos de divergência em relação ao upstream. [cite:13][cite:21][cite:22][cite:23]

A solução prioriza overrides em camadas estáveis e com menor atrito de upgrade, como configuração Python, templates, branding, assets estáticos, imagem Docker customizada, parâmetros de deploy e empacotamento do tema. Overrides mais profundos em frontend React são admitidos apenas como exceção, quando não houver mecanismo suportado ou sustentável em camadas superiores. [cite:21][cite:22][cite:23]

Contexto e motivação
====================

O Apache Superset é uma plataforma open source voltada à exploração de dados, construção de gráficos e dashboards, com opções amplas de configuração e implantação, incluindo execução via Docker e customizações por imagem própria e arquivos de configuração. Esse perfil o torna mais aderente a cenários em que a organização necessita controlar branding, operação e integrações de forma mais próxima à engenharia de plataforma. [cite:21][cite:22][cite:27]

O Design System do governo brasileiro tem como objetivo garantir consistência e experiência unificada nos serviços digitais, oferecendo padrões, componentes e orientação de uso para designers e desenvolvedores. Uma adaptação institucional do Superset para esse ecossistema exige não apenas troca de logotipo ou cores, mas uma política de aderência visual e comportamental aos princípios do DS-BR. [cite:26][cite:29][cite:32]

Requisitos arquiteturais
========================

Requisitos funcionais
---------------------

* Permitir white-label institucional quase total, com identidade visual baseada no DS-BR. [cite:13][cite:26][cite:32]
* Suportar autenticação configurável, contemplando login local do Superset, OAuth2, LDAP e integração com SSO gov.br por meio do acesso.gov.br, tratado inicialmente como fluxo baseado em OAuth2/OIDC. [cite:21][cite:31]
* Permitir uso interno da interface do Superset e consumo por embeds públicos e privados em aplicações como Django e Moodle. [cite:21][cite:27]
* Suportar implantação em ambientes separados de desenvolvimento e produção. [cite:22][cite:27]

Requisitos não funcionais
-------------------------

* Minimizar manutenção evolutiva, evitando fork do frontend sempre que possível. [cite:21][cite:23]
* Preservar compatibilidade com o upstream do Apache Superset e sua licença Apache-2.0. [cite:21][cite:22]
* Permitir empacotamento e publicação automatizada por GitHub Actions. [cite:22]
* Manter rastreabilidade de versões da aplicação e do tema institucional de forma desacoplada. [cite:22]
* Ser compatível com reverse proxy aderente a padrões de mercado, como Nginx ou Traefik. [cite:27][cite:30]

Decisão arquitetural
====================

Alternativas consideradas
-------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Critério
     - Apache Superset
     - Metabase OSS
   * - Customização estrutural e branding
     - Melhor perspectiva de evolução de theming e uso de imagem/configuração própria. [cite:13][cite:21][cite:23]
     - Branding oficial concentrado em recursos pagos; OSS com forte limitação para personalização profunda. [cite:11][cite:12][cite:19]
   * - Aderência a white-label institucional
     - Mais adequada para estratégia por camadas e custom image. [cite:13][cite:22][cite:23]
     - Possível apenas com embed, hacks ou fork, com menor previsibilidade. [cite:12][cite:15][cite:16]
   * - Manutenção sem fork
     - Viável como estratégia principal. [cite:21][cite:23]
     - Limitada para objetivos de identidade institucional forte. [cite:11][cite:12]
   * - Flexibilidade técnica
     - Alta, especialmente para equipes com perfil de infraestrutura e desenvolvimento. [cite:21][cite:22]
     - Mais simples para uso rápido, porém menos moldável no OSS. [cite:11][cite:12]
   * - Embeds
     - Suportados, inclusive em cenários autenticados e integrados. [cite:21][cite:27]
     - Também suportados, com customização mais conveniente no contexto de modular embeds. [cite:15]

Escolha adotada
---------------

Foi adotado o Apache Superset como plataforma-base da solução. A decisão decorre da necessidade de white-label institucional quase total, baixa tolerância a manutenção corretiva associada a forks extensos e preferência por uma estratégia de customização em camadas compatíveis com o upstream. [cite:13][cite:21][cite:23]

O Metabase permanece tecnicamente válido como ferramenta de BI para cenários de rápida adoção, porém não foi selecionado para esta iniciativa porque sua edição open source não oferece, de forma nativa e sustentável, o grau de controle visual e estrutural requerido por um produto institucional alinhado ao DS-BR. A própria documentação e discussões da comunidade apontam que branding completo é tratado como recurso pago e que não existe mecanismo suportado de injeção geral de CSS na aplicação OSS. [cite:11][cite:12][cite:19]

Registro ADR-001
~~~~~~~~~~~~~~~~

* **Título:** Seleção do Apache Superset como base para solução institucional DS-BR
* **Status:** Aprovado
* **Contexto:** Necessidade de plataforma open source com white-label institucional quase total, mínima divergência de upstream, autenticação configurável, embeds públicos e privados, deploy em Docker Compose e trilha futura para Kubernetes. [cite:21][cite:22][cite:27][cite:30]
* **Decisão:** Adotar Apache Superset, customizado por camadas de override de baixo atrito. [cite:13][cite:21][cite:23]
* **Consequências:** Maior esforço inicial de engenharia do que ferramentas mais prontas, porém melhor aderência à identidade institucional e maior governabilidade técnica. [cite:13][cite:21]

Princípios de arquitetura
=========================

* **Upstream-first:** toda customização deve priorizar mecanismos suportados, documentados e reprodutíveis. [cite:21][cite:22]
* **Sem fork por padrão:** alterações profundas de frontend devem ser evitadas e só admitidas quando houver justificativa formal. [cite:23]
* **Design system first:** a identidade DS-BR deve orientar tokens visuais, componentes e padrões de navegação. [cite:26][cite:29][cite:32]
* **Configuração como código:** parâmetros de autenticação, branding, deploy e ambientes devem ser versionados. [cite:21][cite:22][cite:27]
* **Evolução controlada:** releases devem ser rastreáveis, com compatibilidade explícita entre aplicação e tema institucional. [cite:22]

Arquitetura lógica
==================

A arquitetura lógica é composta por sete domínios principais: interface Superset, camada de tema institucional, autenticação e autorização, serviços de dados e metadados, cache, publicação por embeds e automação de entrega. O comportamento visual da aplicação deriva da combinação entre Superset upstream, configuração institucional e pacote de tema DS-BR, preservando a separação entre núcleo da plataforma e personalizações do projeto. [cite:13][cite:21][cite:23]

A autenticação é tratada como configurável, com início operacional em OAuth2 e suporte arquitetural documentado para login local, LDAP e acesso.gov.br. A opção por não adotar JWT como mecanismo inicial busca reduzir complexidade e acelerar a primeira entrega, sem bloquear evolução futura para cenários específicos de integração. [cite:21][cite:31]

.. mermaid::

    flowchart TD
        U[Usuário] --> RP[Reverse Proxy\nNginx ou Traefik]
        RP --> S[Apache Superset]
        S --> T[Tema Institucional DS-BR]
        S --> A[Camada de Autenticação]
        A --> O[OAuth2 / acesso.gov.br]
        A --> L[LDAP]
        A --> D[Login local]
        S --> M[PostgreSQL Metadata DB]
        S --> C[Valkey]
        S --> E[Embeds públicos e privados]
        E --> DJ[Django]
        E --> MO[Moodle]
        CI[GitHub Actions] --> IMG[Imagem customizada]
        IMG --> S

Arquitetura física
==================

Implantação base
----------------

A implantação base em produção e desenvolvimento utiliza Apache Superset com PostgreSQL para banco de metadados, Valkey para cache e suporte operacional, além de reverse proxy compatível com Nginx ou Traefik. O modelo é compatível com as abordagens documentadas de configuração e uso de Docker no ecossistema do Superset. [cite:21][cite:22][cite:27]

Ambientes
---------

São previstos dois ambientes formais: desenvolvimento e produção. O ambiente de desenvolvimento receberá artefatos associados a draft release/tag com sufixo ``-dev``, enquanto o ambiente de produção receberá artefatos de releases finais estáveis. [cite:22]

.. mermaid::

    flowchart LR
        DEV[Git tag/release vX.Y.Z-dev] --> GHA1[GitHub Actions - Dev]
        GHA1 --> REG1[Registry de imagens]
        REG1 --> ENV1[Ambiente Desenvolvimento]

        PRD[Git release vX.Y.Z] --> GHA2[GitHub Actions - Produção]
        GHA2 --> REG2[Registry de imagens]
        REG2 --> ENV2[Ambiente Produção]

Arquitetura futura de referência
--------------------------------

Kubernetes é definido neste DAS como arquitetura futura ou referencial, e não como baseline inicial. Essa decisão preserva simplicidade operacional no curto prazo e reduz custo de manutenção, ao mesmo tempo em que mantém espaço para evolução em cenários de escalabilidade, alta disponibilidade e governança mais avançada de workloads. [cite:22][cite:30]

Estratégia de customização
==========================

A estratégia de customização foi definida em ordem de preferência, sempre do mecanismo menos invasivo para o mais invasivo. O objetivo é atender ao white-label institucional quase total preservando o maior grau possível de compatibilidade com as releases do Apache Superset. [cite:13][cite:21][cite:23]

Ordem de adoção recomendada:

1. Configuração oficial e parâmetros do Superset. [cite:21]
2. Assets, logotipos, favicon e arquivos estáticos empacotados em imagem própria. [cite:23]
3. Templates e camadas de branding suportadas. [cite:23]
4. Tema institucional versionado separadamente da aplicação. [cite:13][cite:22]
5. Overrides localizados de frontend, apenas mediante ADR específica. [cite:13][cite:23]

Pontos de override
==================

Matriz de overrides
-------------------

.. list-table::
   :widths: 15 20 20 15 10 10 10
   :header-rows: 1

   * - Camada
     - Objetivo
     - Mecanismo preferencial
     - Exemplo de artefato
     - Impacto em upgrade
     - Risco
     - Recomendação
   * - Reverse proxy
     - Cabeçalhos, TLS, roteamento, CSP, paths
     - Configuração Nginx/Traefik
     - ``infra/proxy/``
     - Baixo
     - Baixo
     - Padrão
   * - Build/Imagem
     - Empacotar assets e config institucional
     - Dockerfile customizado
     - ``docker/Dockerfile``
     - Baixo a médio
     - Baixo
     - Padrão
   * - Configuração Python
     - Autenticação, branding, flags e integrações
     - ``superset_config.py``
     - ``config/superset_config.py``
     - Baixo
     - Baixo
     - Padrão
   * - Assets estáticos
     - Logo, favicon, imagens e CSS complementar
     - Pasta de assets empacotada
     - ``theme/assets/``
     - Baixo
     - Baixo
     - Padrão
   * - Templates
     - Ajustes controlados de telas, como login
     - Template override localizado
     - ``theme/templates/``
     - Médio
     - Médio
     - Preferível antes de fork
   * - Tokens visuais
     - Cores, fontes, espaçamento, DS-BR
     - CSS institucional versionado
     - ``theme/css/dsbr-theme.css``
     - Médio
     - Médio
     - Usar com parcimônia
   * - Embeds
     - Aparência e integração externa
     - Configuração por portal host
     - ``embeds/``
     - Baixo
     - Baixo
     - Padrão
   * - Frontend React
     - Alterações profundas de componentes
     - Patch/fork localizado
     - ``patches/`` ou fork
     - Alto
     - Alto
     - Exceção

Diretrizes por camada
---------------------

Reverse proxy
~~~~~~~~~~~~~

O reverse proxy deverá concentrar responsabilidades de TLS, segurança perimetral, políticas de headers, compressão, roteamento e eventuais ajustes de path para publicação. Essa camada é estratégica porque permite resolver parte importante das exigências institucionais sem tocar no núcleo do Superset. [cite:27][cite:30]

Imagem customizada
~~~~~~~~~~~~~~~~~~

A imagem customizada será o principal mecanismo de empacotamento do tema institucional, dos assets DS-BR, do arquivo ``superset_config.py`` e de ajustes de templates aceitos no baseline. A documentação do Superset orienta o uso de imagens próprias e customização de builds em cenários não triviais ou produtivos. [cite:22][cite:30]

Configuração Python
~~~~~~~~~~~~~~~~~~~

A camada de configuração Python será o ponto principal de parametrização de autenticação, branding, integrações e flags de comportamento. Essa abordagem reduz o acoplamento com o frontend e aumenta a rastreabilidade da configuração institucional. [cite:21][cite:31]

Templates e branding
~~~~~~~~~~~~~~~~~~~~

A customização de logo, favicon e partes da experiência visual deve ser feita prioritariamente por assets e templates controlados, evitando alterações mais profundas do frontend. A prática reportada pela comunidade para logos e favicons em cenários Docker reforça esse caminho como o mais futuro-compatível. [cite:23]

Frontend profundo
~~~~~~~~~~~~~~~~~

Overrides em componentes React ou patches em código upstream só devem ocorrer quando a exigência institucional não puder ser resolvida por configuração, assets ou templates. Cada caso deverá ser formalizado por decisão arquitetural específica, com análise de impacto de upgrade, rollback e custo de manutenção. [cite:13][cite:23]

Autenticação e segurança
========================

A solução deverá suportar autenticação configurável, contemplando login local, OAuth2, LDAP e integração com acesso.gov.br como mecanismo de SSO baseado em OAuth2/OIDC. O baseline funcional da primeira entrega adotará OAuth2 como abordagem prioritária, registrando a não adoção inicial de JWT como simplificação deliberada. [cite:21][cite:31]

Essa escolha reduz complexidade de implementação, facilita governança da autenticação em ambiente institucional e preserva possibilidade de evolução futura para cenários em que JWT se torne necessário para integrações específicas. Em embeds privados, recomenda-se alinhamento com o portal hospedeiro para evitar duplicidade de sessão e fluxos paralelos de autenticação. [cite:21][cite:27]

Embeds
======

O projeto deverá oferecer suporte a embeds públicos e privados. Para embeds privados, a preferência arquitetural é que o contexto de autenticação e autorização seja coordenado pela aplicação hospedeira, como Django ou Moodle, de modo a reduzir inconsistências de identidade, permissões e experiência do usuário. [cite:21][cite:27]

No caso de embeds públicos, o DAS recomenda especial atenção a políticas de cache, exposição mínima de dados, cabeçalhos de segurança, limitação de escopo e critérios de publicação. Esses itens deverão ser refletidos na configuração do reverse proxy e nas políticas de governança de dashboards. [cite:27][cite:30]

CI/CD e versionamento
=====================

O pipeline CI/CD será implementado explicitamente em GitHub Actions, com build, empacotamento, validação e publicação da solução. O fluxo aprovado é: draft release/tag ``vX.Y.Z-dev`` para build e deploy em desenvolvimento; release/tag ``vX.Y.Z`` para build e deploy em produção. [cite:22]

Recomenda-se separar o versionamento da solução e do tema institucional. Assim, a aplicação poderá ser identificada por uma versão de distribuição e o tema por uma versão própria, com matriz explícita de compatibilidade, por exemplo: solução ``1.4.0`` compatível com tema institucional ``1.2.0`` sobre Apache Superset ``6.0.x``. [cite:13][cite:22]

Política sugerida de versionamento
----------------------------------

.. list-table::
   :widths: 30 30 40
   :header-rows: 1

   * - Artefato
     - Convenção sugerida
     - Destino
   * - Solução integrada
     - ``vX.Y.Z-dev``
     - Desenvolvimento
   * - Solução integrada
     - ``vX.Y.Z``
     - Produção
   * - Tema institucional
     - ``theme-vA.B.C-dev``
     - Desenvolvimento
   * - Tema institucional
     - ``theme-vA.B.C``
     - Produção
   * - Compatibilidade
     - ``Superset 6.0.x + Theme 1.2.x``
     - Matriz documental

Estrutura de pastas sugerida
----------------------------

.. code-block:: text

    superset-institucional-ds-br/
    ├── .github/
    │   └── workflows/
    │       ├── build-dev.yml
    │       └── build-prod.yml
    ├── config/
    │   └── superset_config.py
    ├── docker/
    │   ├── Dockerfile
    │   └── docker-compose.yml
    ├── infra/
    │   └── proxy/
    │       ├── nginx/
    │       └── traefik/
    ├── theme/
    │   ├── assets/
    │   │   ├── img/
    │   │   ├── favicon/
    │   │   └── fonts/
    │   ├── css/
    │   │   └── dsbr-theme.css
    │   ├── templates/
    │   │   └── login/
    │   └── manifest/
    ├── embeds/
    │   ├── django/
    │   └── moodle/
    ├── docs/
    │   ├── adr/
    │   ├── diagrams/
    │   └── compatibility-matrix.md
    └── patches/

Matriz de componentes
=====================

.. list-table::
   :widths: 20 30 20 30
   :header-rows: 1

   * - Componente
     - Papel arquitetural
     - Tecnologia
     - Observações
   * - Plataforma analítica
     - Core da solução
     - Apache Superset
     - Base da aplicação. [cite:21]
   * - Banco de metadados
     - Persistência de configuração e estado
     - PostgreSQL
     - Banco previsto para o projeto. [cite:21][cite:27]
   * - Cache
     - Cache e suporte operacional
     - Valkey
     - Compatível com papel normalmente exercido por Redis-like. [cite:21]
   * - Proxy reverso
     - Entrada HTTP, TLS e headers
     - Nginx ou Traefik
     - Camada perimetral compatível. [cite:27][cite:30]
   * - Autenticação
     - Login local, OAuth2, LDAP, acesso.gov.br
     - Flask AppBuilder / provedores
     - Configurável por ambiente. [cite:21][cite:31]
   * - Tema institucional
     - Branding e aderência DS-BR
     - Assets, CSS, templates
     - Separado da aplicação. [cite:23][cite:26][cite:32]
   * - Portal hospedeiro de embed
     - Consumo externo autenticado ou público
     - Django e Moodle
     - Casos previstos. [cite:21][cite:27]
   * - CI/CD
     - Build e deploy
     - GitHub Actions
     - Fluxo por tags e releases. [cite:22]

Riscos arquiteturais
====================

.. list-table::
   :widths: 10 40 15 15 20
   :header-rows: 1

   * - ID
     - Risco
     - Probabilidade
     - Impacto
     - Resposta
   * - R1
     - Necessidade de override profundo em frontend para aderência completa ao DS-BR
     - Média
     - Alto
     - Priorizar camadas superiores; formalizar ADR antes de patch.
   * - R2
     - Incompatibilidade entre nova release upstream e tema institucional
     - Média
     - Alto
     - Manter matriz de compatibilidade e checklist de upgrade.
   * - R3
     - Complexidade de autenticação em múltiplos modos
     - Média
     - Médio
     - Habilitar por ambiente e começar com OAuth2.
   * - R4
     - Exposição indevida em embeds públicos
     - Média
     - Alto
     - Endurecer governança de publicação, proxy e políticas de acesso.
   * - R5
     - Acoplamento excessivo entre versão da solução e do tema
     - Média
     - Médio
     - Versionamento desacoplado com compatibilidade explícita.
   * - R6
     - Escalada prematura para Kubernetes sem maturidade operacional
     - Baixa
     - Médio
     - Manter Compose como baseline e K8s como referência futura.

Governança de atualização
=========================

Toda atualização do Apache Superset deverá passar por avaliação prévia de compatibilidade com a camada de tema institucional, templates, autenticação e embeds. A governança de atualização deverá considerar análise de breaking changes, atualização de matriz de compatibilidade e validação em ambiente de desenvolvimento antes de promoção para produção. [cite:21][cite:22][cite:30]

Mudanças que impliquem override profundo, alteração no fluxo de login, mudança relevante de navegação ou adoção de novo mecanismo de autenticação deverão ser acompanhadas de ADR específica. Essa política é necessária para manter a rastreabilidade institucional e proteger a sustentabilidade do projeto ao longo do tempo. [cite:21][cite:31]

Checklist de upgrade
====================

* Validar versão-alvo do Apache Superset e notas de release. [cite:22]
* Confirmar compatibilidade da imagem customizada com a nova versão. [cite:22][cite:30]
* Revalidar ``superset_config.py`` e parâmetros de autenticação. [cite:21][cite:31]
* Revalidar assets, logos, favicon e CSS institucional. [cite:23]
* Testar templates customizados, especialmente login e branding. [cite:23]
* Executar testes de embeds públicos e privados em Django e Moodle. [cite:21][cite:27]
* Validar políticas no reverse proxy, headers e CSP. [cite:27][cite:30]
* Atualizar matriz de compatibilidade entre solução, tema e upstream. [cite:22]
* Publicar release ``-dev``, validar em desenvolvimento e somente depois promover para produção. [cite:22]

Seções hands-on
===============

Exemplo de baseline de override
-------------------------------

Os arquivos abaixo representam a linha-base mínima de customização do projeto:

* ``config/superset_config.py`` para autenticação, branding e parâmetros institucionais.
* ``theme/assets/`` para logotipos, favicons e recursos visuais.
* ``theme/css/dsbr-theme.css`` para tokens e ajustes visuais alinhados ao DS-BR.
* ``theme/templates/`` para overrides localizados, com prioridade para tela de login e branding institucional.
* ``docker/Dockerfile`` para empacotamento reprodutível da solução. [cite:21][cite:22][cite:23][cite:26]

Regras práticas para override
-----------------------------

* Não alterar o código upstream sem antes esgotar configuração, assets e templates. [cite:21][cite:23]
* Todo override deve ser rastreável por diretório, versão e justificativa. [cite:22]
* Todo override que impacte upgrade deve possuir estratégia documentada de teste e rollback. [cite:22][cite:30]
* Toda necessidade de patch React deve gerar ADR própria. [cite:13][cite:23]

Conformidade de licenciamento
=============================

O projeto deverá preservar compatibilidade com a licença Apache-2.0, em alinhamento com a licença do Apache Superset. O uso de tema institucional, assets próprios e empacotamento em imagem customizada deverá respeitar as obrigações de atribuição e manutenção dos avisos de licença aplicáveis. [cite:21][cite:22]

Considerações finais
====================

A arquitetura aqui definida equilibra identidade institucional forte, aderência ao DS-BR, governabilidade de software open source e pragmatismo operacional. A decisão por Apache Superset, combinada com estratégia de override em camadas e aversão explícita a forks profundos, constitui a base mais sustentável para entregar uma solução institucional de analytics com identidade visual própria e potencial de evolução controlada. [cite:13][cite:21][cite:23][cite:32]
