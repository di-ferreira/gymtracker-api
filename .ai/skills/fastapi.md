# FastAPI Standards

## Estrutura

Routers:

api/routers

Schemas:

schemas/

Services:

services/

Repositories:

repositories/

---

# Versionamento

Utilizar:

/api/v1

Preparar:

/api/v2

---

# Responses

Toda resposta deve possuir schema.

Nunca retornar:

dict

list

sem tipagem

---

# Dependency Injection

Utilizar Depends.

Exemplo:

get_db

get_exercise_service

---

# Exceptions

Criar exceções customizadas.

Exemplos:

ExerciseNotFoundException

MuscleGroupNotFoundException

CatalogVersionNotFoundException

---

# Paginação

Padrão:

page

limit

---

# Busca

Padrão:

search

---

# Ordenação

Padrão:

sort

order

---

# OpenAPI

Todos endpoints devem possuir:

summary

description

response_model

tags

---

# Status Codes

200

201

204

400

404

409

422

500

Utilizar corretamente.

---

# Health Check

Obrigatório.

Endpoint:

GET /health

---

# Logs

Preparar integração futura.

Não utilizar print.
