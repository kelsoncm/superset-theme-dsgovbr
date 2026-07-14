# Dockerfile customizado para SupersetBR
# Baseado na imagem oficial do Apache Superset
# Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.

ARG SUPERSET_VERSION=4.0.2
FROM apache/superset:${SUPERSET_VERSION}

USER root

# Instalar dependências necessárias para autenticação OAuth/LDAP (se necessário)
# O Apache Superset oficial já traz os pacotes principais, mas garantimos atualizações
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de configuração institucional
COPY --chown=superset:superset ./config/superset_config.py /app/pythonpath/superset_config.py

# Injetar assets estáticos do tema DSGovBR (CSS e Logos)
# Copiamos para o diretório static mapeado pelo Flask-AppBuilder/Superset
COPY --chown=superset:superset ./theme/css/dsgovbr-theme.css /app/superset/static/assets/stylesheets/dsgovbr-theme.css
COPY --chown=superset:superset ./theme/assets/img/logo-dsgovbr.jpg /app/superset/static/assets/images/logo-dsgovbr.jpg
COPY --chown=superset:superset ./theme/assets/favicon/favicon.jpg /app/superset/static/assets/images/favicon.jpg

# Sobrescrever templates de visualização do Flask-AppBuilder
COPY --chown=superset:superset ./theme/templates/appbuilder/ /app/superset/templates/appbuilder/

# Garantir variáveis de ambiente corretas
ENV SUPERSET_CONFIG_PATH=/app/pythonpath/superset_config.py
ENV FLASK_ENV=production

USER superset
