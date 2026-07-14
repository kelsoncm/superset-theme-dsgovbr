# Matriz de Compatibilidade do SupersetBR

Este documento registra a compatibilidade entre as versões do tema institucional **DSGovBR** e as imagens upstream do **Apache Superset**, além do status das releases integradas.

---

## 1. Matriz de Versões

| Versão do Tema | Versão do Superset (Upstream) | Versão SupersetBR (Integrada) | Status | Notas |
| :--- | :--- | :--- | :--- | :--- |
| `theme-v1.0.0` | `4.0.2` | `v1.0.0` | **Estável** | Release de baseline inicial com suporte a OAuth2 e Nginx. |
| `theme-v1.0.0-dev` | `4.0.2` | `v1.0.0-dev` | **Em Desenvolvimento** | Rastreamento de alterações em ambiente de desenvolvimento. |

---

## 2. Componentes e Tecnologias Homologadas

* **Banco de Metadados:** PostgreSQL 15+
* **Cache / Broker:** Valkey 7.2+
* **Proxy Reverso:** Nginx 1.25+ ou Traefik 2.10+
* **Autenticação:**
  * Login Local (`AUTH_DB`)
  * OAuth2 / OIDC (`acesso.gov.br` integrado)
  * LDAP

---

## 3. Histórico de Testes e Validação

### Validação da v1.0.0 (2026-07-14)
* **Status:** Aprovado.
* **Componentes Testados:**
  * Override de CSS em `theme/css/dsgovbr-theme.css`.
  * Redirecionamento e injeção do cabeçalho base `baselayout.html`.
  * Tela de login customizada com suporte a botão gov.br.
  * Integração com Valkey 7.2 no docker-compose.
