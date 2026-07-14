# Política de Segurança (SECURITY.md)

Este documento define as diretrizes para relatar vulnerabilidades de segurança e descreve a política de atualizações de segurança para o projeto **SupersetBR**.

---

## 1. Versões Suportadas

Apenas as seguintes versões da nossa distribuição recebem atualizações ativas de segurança:

| Versão | Suportado |
| :--- | :---: |
| `v1.x` | Sim |
| `< v1.0` | Não |

Como o **SupersetBR** estende a imagem oficial do **Apache Superset**, recomendamos manter a imagem atualizada com as tags estáveis upstream mais recentes, conforme detalhado no nosso manual de [compatibility-matrix.md](file:///C:/Users/2080882/projetos/PESSOAL/superset-theme-dsgovbr/docs/compatibility-matrix.md).

---

## 2. Como Relatar uma Vulnerabilidade

**Por favor, não abra issues públicas no GitHub para relatar problemas ou brechas de segurança.**

Se você identificar uma falha de segurança no SupersetBR, solicitamos que nos envie um relatório detalhado por e-mail de maneira privada para que possamos analisar e corrigir o problema antes de sua divulgação pública.

* **E-mail para contato:** `seguranca@supersetbr.gov.br` (fictício/institucional)

### O que incluir no seu relatório:

* Descrição detalhada da vulnerabilidade encontrada.
* Passos necessários para reproduzir a falha (Proof of Concept - PoC).
* O impacto potencial da falha (ex: vazamento de dados, negação de serviço, bypass de autenticação).
* Sugestões de correção, se houver.

---

## 3. Nosso Processo de Resposta

Ao recebermos uma notificação privada de segurança, nos comprometemos a seguir o seguinte fluxo:

1. **Confirmação de recebimento:** Enviaremos uma resposta inicial confirmando o recebimento em até **48 horas úteis**.
2. **Análise e Validação:** Analisaremos o relatório para confirmar a existência da falha e estimar o impacto.
3. **Desenvolvimento da Correção:** Desenvolveremos uma correção adequada no ambiente de desenvolvimento (`-dev`).
4. **Publicação da Release:** Publicaremos a correção em uma nova tag Git (`vX.Y.Z`) e notificaremos os responsáveis pelo reporte.
5. **Divulgação:** Se necessário, divulgaremos a vulnerabilidade e daremos o devido crédito aos pesquisadores de segurança.
