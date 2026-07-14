# AGENTS.md – SupersetBR (caveman)

Repositório é **SupersetBR**.  
Base é **Apache Superset**.  
Cara tem que ser **DSGovBR**.

Não quebrar upstream. Não inventar moda sem olhar o documento.

---

## 1. Antes de tudo

- Sempre ler o DAS `docs/documento-arquitetura-software.md`.
- Se mudança for grande (auth, deploy, tema), tem que bater com o DAS.  
- Se decisão é arquitetural, criar/atualizar ADR em `docs/adr/`.

---

## 2. Onde mexer

- Comportamento do Superset → `config/superset_config.py`.
- Deploy / imagem → `docker/Dockerfile` e `docker/docker-compose.yml`.
- Proxy, TLS, headers → `infra/proxy/`.
- Tema DSGovBR → `theme/`:
  - `theme/assets/` → logo, favicon, imagens, fontes.
  - `theme/css/dsgovbr-theme.css` → cores, fontes, espaçamentos DSGovBR.
  - `theme/templates/` → tela de login e branding.

- Embeds:
  - `embeds/django/` → exemplo Django.
  - `embeds/moodle/` → exemplo Moodle.

---

## 3. Regras caveman

1. **Não forkar frontend sem dor real**  
   - Primeiro tentar:
     - config (`superset_config.py`),  
     - assets,  
     - CSS,  
     - templates,  
     - Dockerfile.

2. **DAS manda**  
   - Mudança contra o DAS → errado.  
   - Atualizar DAS se arquitetura mudar, mas apenas se explicitamente autorizado.

3. **Tudo com trilha**  
   - Decisão grande → ADR em `docs/adr/`.
   - Nada escondido em script solto.

---

## 4. Autenticação

- Coisas que valem hoje:
  - Login local (AUTH_DB).
  - OAuth2/OIDC (acesso.gov.br incluído).
  - LDAP.

- Regra:
  - Começa simples: OAuth2 primeiro.
  - JWT só entra se tiver ADR dizendo “por quê” e DAS atualizado.

- Onde mexer:
  - `superset_config.py`.  
  - Usar env var pra segredos e endpoints, nada hardcoded.

---

## 5. Tema DSGovBR

Prioridade de onde mexer (do mais seguro pro mais arriscado):

1. `superset_config.py` (config oficial).
2. `theme/assets/` (imagens, logos).
3. `theme/css/dsgovbr-theme.css` (tokens e layout).
4. `theme/templates/` (login, branding).
5. React/frontend → só em último caso, com ADR.

Regras:

- Seguir padrão DSGovBR (cores, contraste, acessibilidade).
- Nome de classe e token limpos, sem gambiarras.  
- Mudou tema → atualizar manifest e, se preciso, DAS (mas o DAS precisa de autorização expressa).

---

## 6. Deploy

- Hoje:
  - Baseline é **Docker Compose**.
  - PostgreSQL = metadados.  
  - Valkey = cache.  
  - Proxy = Nginx ou Traefik.

- Kubernetes:
  - Futuro, não presente.
  - Se criar YAML, marcar como “referencial”, não “oficial”.

- Regra pra agente:
  - Compose tem que subir tudo e funcionar.  
  - Não criar 3 Compose diferentes. Se precisar, usar override.

---

## 7. CI/CD e versões

- Usa **GitHub Actions**.

Fluxo:

- Tag `vX.Y.Z-dev` → build + deploy em dev.  
- Tag `vX.Y.Z` → build + deploy em produção.

Tema:

- Tema DSGovBR tem versão própria: `theme-vA.B.C`.  
- Matriz de compatibilidade fica em `docs/compatibility-matrix.md`.

Agente faz:

- Ajusta `.github/workflows/` quando mexe em pipeline.  
- Segue esquema de versão, não inventa outro.  
- Mudança grande em CI/CD → atualizar DAS (mas apenas se explicitamente autorizado) e ADR.

---

## 8. Embeds

- Tipos:
  - Público.  
  - Privado (via portal, ex.: Django, Moodle).

Regras:

- Reusar exemplos de `embeds/django/` e `embeds/moodle/`.  
- Auth principal deve ficar no portal, não duplicar auth no Superset e no host.
- Garantir headers e CSP decentes no proxy.

---

## 9. Estilo

- Código claro, configurável via env.
- Comentário explica decisão, não reexplica óbvio.  
- Docs em português Brasil, tom institucional, mas direto.  
- Mudança de arquitetura → atualizar DAS (mas apenas se explicitamente autorizado) e ADR, não só código.

---

## 10. Como usar agente direito

Use agente para:

- Gerar/ajustar:
  - `superset_config.py`,  
  - Docker/Compose,  
  - CSS do tema,  
  - exemplos de embed.

- Escrever:
  - ADR nova,  
  - trecho de DAS (mas apenas se explicitamente autorizado),  
  - workflow do GitHub Actions.

Sempre falar pro agente:

- “Leia `AGENTS.md` antes de mexer.”
