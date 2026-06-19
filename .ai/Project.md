# GymTracker API

## Objetivo

API responsável pelo gerenciamento do catálogo de exercícios do GymTracker.

Esta API fornece dados para:

* Aplicativo Mobile
* Painel Administrativo

## Stack Oficial

* Python 3.13
* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Alembic
* Pydantic v2
* Docker
* Docker Compose
* Pytest

## Arquitetura

Seguir obrigatoriamente:

* Clean Architecture
* SOLID
* Repository Pattern
* Service Layer
* Dependency Injection

## Estrutura de Camadas

Controller
↓
Service
↓
Repository
↓
Database

## Regras Gerais

* Nenhuma regra de negócio em Controllers
* Nenhum acesso direto ao banco fora dos Repositories
* Toda validação deve ser feita via Schemas
* Toda resposta deve ser tipada
* Toda migration deve utilizar Alembic

## Domínio Principal

Exercícios físicos

Equipamentos

Grupos musculares

Grupos de movimento

Substituições de exercícios

Versionamento de catálogo

## Escopo Atual

Catálogo de exercícios

Não implementar:

* Login
* JWT
* Usuários
* Assinaturas
* IA em runtime

## Escopo Futuro

* Autenticação
* Sincronização de usuário
* Histórico de treinos
* Progressão de carga

## Convenções

Arquivos:

exercise_service.py

exercise_repository.py

exercise_schema.py

exercise_router.py

Classes:

ExerciseService

ExerciseRepository

ExerciseCreateSchema

ExerciseResponseSchema

## Testes

Cobertura mínima:

80%

## Fonte da Verdade

Sempre consultar:

product/*
architecture/*
agents/*
skills/*
