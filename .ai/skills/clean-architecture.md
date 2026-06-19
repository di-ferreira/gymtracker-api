# Clean Architecture

## Objetivo

Garantir separação clara entre:

* HTTP
* Regras de Negócio
* Persistência
* Banco de Dados

---

# Camadas

Router

Responsável por:

* Receber requisições
* Validar entrada
* Retornar resposta

Não deve conter:

* SQL
* Regras de negócio
* Regras de domínio

---

Service

Responsável por:

* Casos de uso
* Regras de negócio
* Orquestração

Pode utilizar:

* Repositories
* Mappers

Não deve acessar banco diretamente.

---

Repository

Responsável por:

* Consultas
* Persistência
* Paginação
* Filtros

Não deve conter regra de negócio.

---

Model

Representação do banco.

Apenas entidades SQLAlchemy.

---

Schema

Entrada e saída da API.

Utilizar Pydantic v2.

---

Mapper

Conversão entre:

Model
↔
Schema

---

# Fluxo Obrigatório

Router
↓
Service
↓
Repository
↓
Database

---

# Dependências

Sempre injetar dependências.

Nunca instanciar repositórios diretamente.

Exemplo:

ExerciseService(
repository
)

---

# SOLID

Aplicar:

* SRP
* OCP
* LSP
* ISP
* DIP

---

# Proibições

Não utilizar:

* lógica em routers
* SQL em services
* SQL em routers
* acesso direto ao banco fora dos repositories
