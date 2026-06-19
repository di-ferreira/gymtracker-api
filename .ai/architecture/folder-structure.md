# Estrutura Oficial da API

src/

├── api/
│
│   ├── dependencies/
│   │
│   ├── routers/
│   │   ├── health.py
│   │   ├── exercises.py
│   │   ├── muscle_groups.py
│   │   ├── movement_groups.py
│   │   ├── equipments.py
│   │   └── catalog.py
│
│   └── api.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── exceptions.py
│   └── constants.py
│
├── database/
│   ├── session.py
│   ├── base.py
│   └── migrations/
│
├── models/
│   ├── exercise.py
│   ├── muscle_group.py
│   ├── movement_group.py
│   ├── equipment.py
│   ├── exercise_instruction.py
│   ├── exercise_equipment.py
│   ├── exercise_alternative.py
│   └── catalog_version.py
│
├── repositories/
│   ├── exercise_repository.py
│   ├── muscle_group_repository.py
│   ├── movement_group_repository.py
│   ├── equipment_repository.py
│   └── catalog_repository.py
│
├── services/
│   ├── exercise_service.py
│   ├── muscle_group_service.py
│   ├── movement_group_service.py
│   ├── equipment_service.py
│   └── catalog_service.py
│
├── schemas/
│   ├── exercise.py
│   ├── muscle_group.py
│   ├── movement_group.py
│   ├── equipment.py
│   └── catalog.py
│
├── mappers/
│   ├── exercise_mapper.py
│   └── catalog_mapper.py
│
└── main.py

tests/

├── unit/
├── integration/
└── e2e/
