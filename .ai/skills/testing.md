# Testing Standards

## Framework

Pytest

---

# Estrutura

tests/

unit/

integration/

e2e/

---

# Cobertura

Mínimo:

80%

Ideal:

90%

---

# Unit Tests

Testar:

* Services
* Regras de negócio
* Casos de uso

Não acessar banco.

---

# Integration Tests

Testar:

* Repositories
* Banco
* Queries

Utilizar banco isolado.

---

# E2E Tests

Testar:

* Endpoints
* Fluxos completos

---

# Fixtures

Criar fixtures reutilizáveis.

Exemplos:

exercise_fixture

equipment_fixture

catalog_fixture

---

# Factories

Utilizar factories para criação de entidades.

---

# Nomeação

test_create_exercise

test_update_exercise

test_get_exercise_by_id

---

# Casos Obrigatórios

Exercício encontrado

Exercício não encontrado

Busca vazia

Paginação

Filtros

Substituições

Sincronização

Versionamento

---

# Proibições

Não utilizar:

sleep

dados compartilhados entre testes

dependência entre testes

ordem de execução
