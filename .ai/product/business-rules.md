# Regras de Negócio

## BR001 - Exercício Obrigatório

Todo exercício deve possuir:

* Nome
* Slug
* Descrição
* Grupo muscular principal
* Grupo de movimento

---

## BR002 - Mídias

Todo exercício pode possuir:

* Thumbnail
* Imagem
* GIF
* Vídeo

As mídias são opcionais.

---

## BR003 - Instruções

Todo exercício deve possuir pelo menos uma instrução de execução.

As instruções devem possuir ordem definida.

Exemplo:

1. Posicione-se corretamente
2. Execute o movimento
3. Retorne lentamente

---

## BR004 - Grupo Muscular

Todo exercício deve possuir um grupo muscular principal.

Exemplos:

* Peito
* Costas
* Ombros
* Bíceps
* Tríceps
* Quadríceps
* Posterior
* Glúteos
* Panturrilha
* Abdômen

---

## BR005 - Grupo de Movimento

Todo exercício deve possuir um grupo de movimento.

Valores válidos:

* Push
* Pull
* Legs
* Core

---

## BR006 - Equipamentos

Um exercício pode possuir nenhum ou vários equipamentos.

Exemplos:

* Halter
* Barra
* Cabo
* Máquina
* Banco
* Peso Corporal

---

## BR007 - Exercícios Substitutos

Substituições são cadastradas manualmente.

Não utilizar IA para gerar substituições durante a execução do aplicativo.

---

## BR008 - Exclusão

Não permitir exclusão física.

Utilizar Soft Delete.

Campo:

deleted_at

---

## BR009 - Versionamento

Qualquer alteração no catálogo deve atualizar a versão do catálogo.

Inclui:

* Criação
* Atualização
* Exclusão lógica

---

## BR010 - Sincronização

Aplicativos clientes devem sincronizar catálogo utilizando versionamento.

Nunca baixar catálogo completo sem necessidade.

---

## BR011 - Slug

Slug deve ser único.

Exemplo:

supino-reto

triceps-pulley-barra

rosca-direta

---

## BR012 - Paginação

Toda listagem deve possuir paginação.

---

## BR013 - Busca

Busca deve ser realizada por:

* Nome
* Slug

---

## BR014 - Auditoria

Toda entidade deve possuir:

* created_at
* updated_at
