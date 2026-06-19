# SQLAlchemy 2.0 Standards

## ORM

Utilizar SQLAlchemy 2.0 declarative mapping.

Não utilizar APIs legadas.

---

# Sessões

Sempre utilizar AsyncSession.

---

# Models

Um arquivo por entidade.

Exemplo:

exercise.py

equipment.py

---

# Base

Criar BaseModel comum.

Campos obrigatórios:

id

created_at

updated_at

deleted_at

---

# IDs

Utilizar UUID v7.

Tipo:

UUID

---

# Relacionamentos

Sempre explicitar:

back_populates

lazy strategy

foreign keys

---

# Soft Delete

Todas entidades devem possuir:

deleted_at

Nunca remover fisicamente.

---

# Queries

Todas consultas devem:

ignorar registros deletados

Exemplo:

deleted_at IS NULL

---

# Índices

Criar índices para:

slug

name

foreign keys

---

# Transactions

Operações de escrita devem utilizar transações.

---

# Alembic

Toda alteração de model:

gera migration

Nunca alterar banco manualmente.
