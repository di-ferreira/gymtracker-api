# Security Standards

## Objetivo

Preparar a API para ambiente de produção.

---

# Autenticação

Não implementar agora.

Preparar arquitetura para:

JWT

Refresh Token

RBAC

---

# CORS

Configurar whitelist.

Permitir apenas:

* Mobile App
* Admin Panel

Evitar:

allow_origins=["*"]

em produção.

---

# Secrets

Nunca armazenar:

* Senhas
* Tokens
* Chaves

no código.

Utilizar:

.env

---

# Environment Variables

Obrigatórias:

DATABASE_URL

APP_ENV

SECRET_KEY

API_VERSION

---

# SQL Injection

Utilizar apenas:

SQLAlchemy ORM

Proibido:

SQL concatenado manualmente.

---

# Soft Delete

Nunca remover registros críticos.

Utilizar:

deleted_at

---

# Rate Limiting

Preparar suporte futuro.

Exemplo:

100 requests/minuto

por IP.

---

# Logs

Nunca registrar:

* Senhas
* Tokens
* Headers sensíveis

---

# Error Messages

Não expor:

* Stack Trace
* Queries SQL
* Estrutura interna

Produção:

Mensagem amigável.

---

# Headers

Preparar suporte para:

X-Request-ID

X-Correlation-ID

---

# HTTPS

Produção:

HTTPS obrigatório.

---

# Uploads

Validar:

* extensão
* mime type
* tamanho

---

# Dependências

Atualizar regularmente.

Executar:

* Safety
* Bandit
* Ruff

---

# Auditoria

Registrar:

* criação
* atualização
* exclusão lógica

Campos:

created_at

updated_at

deleted_at

---

# Preparação Futura

RBAC

Roles:

admin

editor

viewer

Estrutura já deve permitir expansão futura.
