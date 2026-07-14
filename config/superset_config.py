# Cuidado: Não quebrar upstream. Leia AGENTS.md antes de mexer.
import os
from flask_appbuilder.security.manager import AUTH_DB, AUTH_OAUTH, AUTH_LDAP

# Configurações Básicas
ROW_LIMIT = int(os.environ.get("ROW_LIMIT", 50000))
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "ALTERE_PARA_UM_VALOR_SEGURO_EM_PRODUCAO")

# Branding Institucional
APP_NAME = os.environ.get("APP_NAME", "SupersetBR")
# Mapeado na imagem Docker a partir de theme/assets/
APP_ICON = "/static/assets/images/logo-dsgovbr.jpg"
APP_ICON_WIDTH = int(os.environ.get("APP_ICON_WIDTH", 150))
FAVICON = "/static/assets/images/favicon.jpg"

# Autenticação
AUTH_TYPE = int(os.environ.get("AUTH_TYPE", AUTH_DB))

# Ativar registro automático de novos usuários pelo OAuth/LDAP se necessário
AUTH_USER_REGISTRATION = os.environ.get("AUTH_USER_REGISTRATION", "True").lower() == "true"
AUTH_USER_REGISTRATION_ROLE = os.environ.get("AUTH_USER_REGISTRATION_ROLE", "Public")

# Configuração de Provedores OAuth
OAUTH_PROVIDERS = []

if AUTH_TYPE == AUTH_OAUTH:
    # Exemplo de configuração padrão para integração com o sso.acesso.gov.br
    # Configurado via variáveis de ambiente para segredos e endpoints
    OAUTH_PROVIDERS = [
        {
            "name": "govbr",
            "icon": "fa-id-card-o",
            "token_key": "access_token",
            "remote_app": {
                "client_id": os.environ.get("OAUTH_CLIENT_ID", ""),
                "client_secret": os.environ.get("OAUTH_CLIENT_SECRET", ""),
                "api_base_url": os.environ.get("OAUTH_API_BASE_URL", "https://sso.staging.acesso.gov.br/"),
                "client_kwargs": {
                    "scope": os.environ.get("OAUTH_SCOPE", "openid email profile govbr_empresa")
                },
                "request_token_url": None,
                "access_token_url": os.environ.get("OAUTH_ACCESS_TOKEN_URL", "https://sso.staging.acesso.gov.br/token"),
                "authorize_url": os.environ.get("OAUTH_AUTHORIZE_URL", "https://sso.staging.acesso.gov.br/authorize"),
            }
        }
    ]

# Configuração de LDAP (se AUTH_TYPE for AUTH_LDAP)
if AUTH_TYPE == AUTH_LDAP:
    AUTH_LDAP_SERVER = os.environ.get("AUTH_LDAP_SERVER", "ldap://localhost:389")
    AUTH_LDAP_USE_TLS = os.environ.get("AUTH_LDAP_USE_TLS", "False").lower() == "true"
    AUTH_LDAP_SEARCH = os.environ.get("AUTH_LDAP_SEARCH", "ou=users,dc=example,dc=com")
    AUTH_LDAP_UID_KEY = os.environ.get("AUTH_LDAP_UID_KEY", "uid")
    AUTH_LDAP_BIND_USER = os.environ.get("AUTH_LDAP_BIND_USER", "cn=admin,dc=example,dc=com")
    AUTH_LDAP_BIND_PASSWORD = os.environ.get("AUTH_LDAP_BIND_PASSWORD", "")

# Configuração de Língua e Localização
LANGUAGES = {
    "pt_BR": {"flag": "br", "name": "Portuguese (Brazil)"},
    "en": {"flag": "us", "name": "English"},
}
BABEL_DEFAULT_LOCALE = os.environ.get("BABEL_DEFAULT_LOCALE", "pt_BR")

# Tema e Overrides de Estilo React (Emotion Theme)
# Alinhado com o Design System do Governo Federal (DSGovBR)
THEME_OVERRIDES = {
    "colors": {
        "primary": {
            "base": "#1351b4",      # Azul Principal do DSGovBR (Active)
            "dark1": "#0c326f",     # Azul Escuro do DSGovBR (Hover)
            "light1": "#2670e8",    # Azul Claro
        },
        "secondary": {
            "base": "#888888",
        },
        "grayscale": {
            "dark2": "#333333",     # Texto Principal (Cinza Escuro)
            "light2": "#f8f8f8",    # Cor de fundo padrão de páginas
        }
    }
}

# Talisman - Segurança de Cabeçalhos HTTP
# Ajustável via variáveis de ambiente
TALISMAN_ENABLED = os.environ.get("TALISMAN_ENABLED", "True").lower() == "true"
TALISMAN_CONFIG = {
    "content_security_policy": None, # CSP flexível, gerenciada preferencialmente pelo Proxy
    "force_https": os.environ.get("TALISMAN_FORCE_HTTPS", "False").lower() == "true",
    "frame_options": "ALLOWFROM" if os.environ.get("TALISMAN_ALLOW_FRAMES", "False").lower() == "true" else "DENY",
}

# Banco de Metadados (PostgreSQL)
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql://superset:superset_password@db:5432/superset"
)

# Cache e Filas de Tarefas (Valkey / Redis)
REDIS_HOST = os.environ.get("REDIS_HOST", "valkey")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

# Flask-Caching configs
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)),
    "CACHE_KEY_PREFIX": "superset_results_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": 1,
}

# Configurações adicionais de Cache do Superset
DATA_CACHE_CONFIG = CACHE_CONFIG
FILTER_STATE_CACHE_CONFIG = CACHE_CONFIG
EXPLORE_FORM_DATA_CACHE_CONFIG = CACHE_CONFIG

