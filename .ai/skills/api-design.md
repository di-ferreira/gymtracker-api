# API Design Standards

## Objetivo

Garantir consistência em todos os endpoints da API.

---

# Base URL

Todas as rotas devem utilizar:

/api/v1

Exemplo:

/api/v1/exercises

/api/v1/muscle-groups

---

# Versionamento

Versão atual:

v1

Preparar estrutura para:

v2

v3

Sem quebrar compatibilidade.

---

# Convenção de Rotas

Utilizar plural.

Correto:

/exercises

/muscle-groups

/equipments

Incorreto:

/exercise

/muscleGroup

/getExercises

---

# HTTP Verbs

GET

Consultar

POST

Criar

PUT

Atualizar completamente

PATCH

Atualização parcial

DELETE

Soft Delete

---

# Paginação

Padrão obrigatório:

?page=1
&limit=20

Resposta:

{
"items": [],
"page": 1,
"limit": 20,
"total": 100,
"total_pages": 5
}

---

# Busca

Parâmetro padrão:

search

Exemplo:

GET /exercises?search=supino

---

# Filtros

Exemplo:

GET /exercises?muscle_group=chest

GET /exercises?equipment=dumbbell

GET /exercises?movement_group=push

Filtros podem ser combinados.

---

# Ordenação

Padrão:

sort
order

Exemplo:

GET /exercises?sort=name&order=asc

Valores:

asc
desc

---

# Response Envelope

Listagens:

{
"items": [],
"page": 1,
"limit": 20,
"total": 100
}

Detalhes:

{
"id": "",
"name": ""
}

---

# Erros

Formato padrão:

{
"error": {
"code": "EXERCISE_NOT_FOUND",
"message": "Exercise not found"
}
}

---

# OpenAPI

Todo endpoint deve possuir:

summary

description

tags

response_model

status_code

---

# Nomenclatura

JSON sempre em snake_case.

Exemplo:

movement_group

created_at

updated_at

---

# Datas

Formato:

ISO 8601

Exemplo:

2026-06-19T10:30:00Z

---

# IDs

UUID v7

Exemplo:

0197d2a2-53f1-7c91-8f8f-4a11fbe2a201

---

# Performance

Listagens nunca devem retornar:

* instruções completas
* alternativas completas
* vídeos

Utilizar endpoint de detalhes.

---

# Cache

Preparar para:

ETag

Last-Modified

Cache-Control

---

# Health Check

Obrigatório:

GET /health

Resposta:

{
"status": "healthy"
}
