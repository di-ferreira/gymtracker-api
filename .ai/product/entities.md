# Entidades

## Exercise

Representa um exercício físico.

Campos:

* id
* name
* slug
* description
* execution_tips
* difficulty
* thumbnail_url
* image_url
* gif_url
* video_url
* movement_group_id
* muscle_group_id
* created_at
* updated_at
* deleted_at

Relacionamentos:

* belongs_to MovementGroup
* belongs_to MuscleGroup
* has_many ExerciseInstruction
* has_many ExerciseEquipment
* has_many ExerciseAlternative

---

## MuscleGroup

Representa um grupo muscular.

Campos:

* id
* name
* slug
* created_at
* updated_at

Exemplos:

* Peito
* Costas
* Ombros

---

## MovementGroup

Representa um grupo de movimento.

Campos:

* id
* name
* slug
* created_at
* updated_at

Exemplos:

* Push
* Pull
* Legs
* Core

---

## Equipment

Representa um equipamento.

Campos:

* id
* name
* slug
* created_at
* updated_at

Exemplos:

* Halter
* Barra
* Cabo
* Máquina

---

## ExerciseEquipment

Relacionamento N:N.

Campos:

* exercise_id
* equipment_id

---

## ExerciseInstruction

Passos para execução.

Campos:

* id
* exercise_id
* step_order
* description

---

## ExerciseAlternative

Relacionamento entre exercícios.

Campos:

* exercise_id
* alternative_exercise_id

Exemplo:

Supino Reto

Alternativas:

* Flexão
* Supino Máquina
* Chest Press

---

## CatalogVersion

Controle de sincronização.

Campos:

* id
* version
* checksum
* created_at

Objetivo:

Permitir sincronização incremental.
