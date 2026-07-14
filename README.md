# SupersetBR

Tema institucional para o Apache Superset alinhado ao Design System do Governo Federal do Brasil (DSGovBR).

---

## 1. Visão Geral

O **SupersetBR** é uma solução de Analytics e Business Intelligence (BI) de código aberto que estende o **Apache Superset** para aplicar a identidade visual, acessibilidade e padrões exigidos pelo **Design System do Governo Federal do Brasil (DSGovBR)**. 

O projeto adota uma estratégia de customização por camadas de override não invasivas, evitando a criação de forks profundos da base de código do Apache Superset e simplificando o processo de atualização (upstream-first).

---

## 2. Estrutura do Repositório

* **`.github/workflows/`**: Pipelines automatizados de CI/CD para compilação e publicação de imagens de Desenvolvimento e Produção.
* **`config/`**: Configuração do Apache Superset (`superset_config.py`), centralizando parâmetros de segurança, autenticação e banco de dados.
* **`docker/`**: Arquivos de containerização (`Dockerfile` e `docker-compose.yml`).
* **`docs/`**: Documentação técnica do projeto estruturada para compilação via **Sphinx**.
* **`embeds/`**: Exemplos práticos de consumo de dashboards privados e seguros para portais em Django e Moodle.
* **`infra/proxy/`**: Configurações do Nginx para publicação e controle de cabeçalhos HTTP/CSP.
* **`theme/`**: Assets de mídia, folhas de estilo CSS (`dsgovbr-theme.css`) e templates do Flask-AppBuilder.

---

## 3. Como Executar (Ambiente Local)

### Pré-requisitos
* Docker Engine 20.10+
* Docker Compose v2.0+

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/kelsoncm/superset-theme-dsgovbr.git
   cd superset-theme-dsgovbr
   ```

2. **Inicie o ambiente de desenvolvimento local:**
   ```bash
   docker compose -f docker/docker-compose.yml up -d
   ```
   
   Isso subirá:
   * **PostgreSQL** na porta `5432` (Metadados).
   * **Valkey** na porta `6379` (Cache e Broker).
   * **SupersetBR** (iniciando migrações de banco e criando o usuário administrador).
   * **Nginx** nas portas `80` e `443` (Proxy reverso e cabeçalhos de segurança).

3. **Acesse a aplicação:**
   Abra o seu navegador em [http://localhost](http://localhost) (passando pelo Proxy Reverso Nginx) ou diretamente em [http://localhost:8088](http://localhost:8088).

   * **Usuário padrão:** `admin`
   * **Senha padrão:** `admin`

---

## 4. Documentação Oficial

A documentação detalhada do projeto está disponível na pasta `docs/`. Ela foi estruturada com o Sphinx.

### Como gerar a documentação em HTML localmente:

1. **Instale as dependências de documentação:**
   ```bash
   pip install sphinx furo
   ```

2. **Gere a documentação:**
   ```bash
   cd docs
   make html
   ```

3. **Visualize no navegador:**
   Abra o arquivo `docs/_build/html/index.html` em seu navegador.

---

## 5. Diretrizes de Desenvolvimento

Antes de realizar contribuições ou modificações no código do repositório, por favor leia com atenção:
* **[AGENTS.md](file:///C:/Users/2080882/projetos\PESSOAL\superset-theme-dsgovbr/AGENTS.md)** — Regras do modo caveman, padrões de deploy e fluxo de CI/CD.
* **[documento-arquitetura-software.md](file:///C:/Users/2080882/projetos\PESSOAL\superset-theme-dsgovbr/docs/documento-arquitetura-software.md)** — Detalhamento técnico da arquitetura lógica, física e matriz de overrides.
