# Modelagem de Banco de Dados

## exercises

| Campo             | Tipo                |
| ----------------- | ------------------- |
| id                | UUID                |
| name              | VARCHAR(255)        |
| slug              | VARCHAR(255) UNIQUE |
| description       | TEXT                |
| execution_tips    | TEXT                |
| difficulty        | VARCHAR(50)         |
| thumbnail_url     | TEXT                |
| image_url         | TEXT                |
| gif_url           | TEXT                |
| video_url         | TEXT                |
| movement_group_id | UUID                |
| muscle_group_id   | UUID                |
| created_at        | TIMESTAMP           |
| updated_at        | TIMESTAMP           |
| deleted_at        | TIMESTAMP NULL      |

Indexes:

* idx_exercise_name
* idx_exercise_slug

---

## muscle_groups

| Campo      | Tipo                |
| ---------- | ------------------- |
| id         | UUID                |
| name       | VARCHAR(100)        |
| slug       | VARCHAR(100) UNIQUE |
| created_at | TIMESTAMP           |
| updated_at | TIMESTAMP           |

---

## movement_groups

| Campo      | Tipo                |
| ---------- | ------------------- |
| id         | UUID                |
| name       | VARCHAR(100)        |
| slug       | VARCHAR(100) UNIQUE |
| created_at | TIMESTAMP           |
| updated_at | TIMESTAMP           |

---

## equipments

| Campo      | Tipo                |
| ---------- | ------------------- |
| id         | UUID                |
| name       | VARCHAR(100)        |
| slug       | VARCHAR(100) UNIQUE |
| created_at | TIMESTAMP           |
| updated_at | TIMESTAMP           |

---

## exercise_equipments

| Campo        | Tipo |
| ------------ | ---- |
| exercise_id  | UUID |
| equipment_id | UUID |

Primary Key:

(exercise_id, equipment_id)

---

## exercise_instructions

| Campo       | Tipo    |
| ----------- | ------- |
| id          | UUID    |
| exercise_id | UUID    |
| step_order  | INTEGER |
| description | TEXT    |

Indexes:

* idx_instruction_order

---

## exercise_alternatives

| Campo                   | Tipo |
| ----------------------- | ---- |
| exercise_id             | UUID |
| alternative_exercise_id | UUID |

Primary Key:

(exercise_id, alternative_exercise_id)

---

## catalog_versions

| Campo      | Tipo         |
| ---------- | ------------ |
| id         | UUID         |
| version    | BIGINT       |
| checksum   | VARCHAR(255) |
| created_at | TIMESTAMP    |

---

# Estratégia de IDs

Utilizar UUID v7.

Motivos:

* Melhor ordenação temporal
* Melhor sincronização futura
* Compatível com escalabilidade

---

# Estratégia de Exclusão

Soft Delete.

Campo:

deleted_at

Nunca remover registros fisicamente.

---

# Estratégia de Índices

Criar índices para:

* slug
* name
* foreign keys

Otimizar:

* busca
* filtros
* sincronização
