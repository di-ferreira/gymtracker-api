# Casos de Uso

## UC001 - Listar Exercícios

Ator:

* Aplicativo Mobile
* Painel Administrativo

Fluxo:

1. Solicita lista de exercícios
2. Aplica filtros opcionais
3. Retorna lista paginada

Resultado:

Lista de exercícios.

---

## UC002 - Consultar Exercício

Ator:

* Aplicativo Mobile

Fluxo:

1. Usuário seleciona exercício
2. Sistema busca detalhes
3. Sistema retorna:

* Nome
* Descrição
* Instruções
* Equipamentos
* GIF
* Vídeo
* Grupo muscular
* Grupo de movimento

Resultado:

Detalhes completos do exercício.

---

## UC003 - Buscar Exercício

Ator:

* Aplicativo Mobile

Fluxo:

1. Usuário informa texto
2. Sistema busca por:

* Nome
* Slug

Resultado:

Lista filtrada.

---

## UC004 - Consultar Exercícios Substitutos

Ator:

* Aplicativo Mobile

Fluxo:

1. Usuário abre exercício
2. Sistema busca substituições cadastradas
3. Sistema retorna alternativas

Resultado:

Lista de exercícios substitutos.

---

## UC005 - Listar Grupos Musculares

Ator:

* Aplicativo Mobile

Resultado:

Lista de grupos musculares.

---

## UC006 - Listar Equipamentos

Ator:

* Aplicativo Mobile

Resultado:

Lista de equipamentos.

---

## UC007 - Sincronizar Catálogo

Ator:

* Aplicativo Mobile

Fluxo:

1. Aplicativo envia versão atual
2. API verifica versão
3. API retorna apenas alterações

Resultado:

Sincronização incremental.

---

## UC008 - Criar Exercício

Ator:

* Administrador

Fluxo:

1. Preenche formulário
2. Salva exercício
3. Atualiza versão do catálogo

Resultado:

Novo exercício cadastrado.

---

## UC009 - Atualizar Exercício

Ator:

* Administrador

Fluxo:

1. Edita exercício
2. Salva alterações
3. Atualiza versão do catálogo

Resultado:

Exercício atualizado.

---

## UC010 - Remover Exercício

Ator:

* Administrador

Fluxo:

1. Solicita remoção
2. Sistema executa soft delete
3. Atualiza versão do catálogo

Resultado:

Exercício ocultado.
