# GymTracker API — Todo List

## Implementado

### Autenticação e Usuários
- [x] Registro (`POST /api/v1/auth/register`)
- [x] Login (`POST /api/v1/auth/login`)
- [x] Perfil atual (`GET /api/v1/auth/me`)
- [x] Atualizar próprio perfil (`PATCH /api/v1/auth/me`) — nome e senha
- [x] Admin listar usuários (`GET /api/v1/admin/users/`)
- [x] Admin atualizar usuário (`PATCH /api/v1/admin/users/{id}`) — role, nome, is_active
- [x] Role-based access control (admin/user)
- [x] JWT com bcrypt

### Catálogo Admin (`/api/v1/admin/catalog`)
- [x] CRUD MuscleGroups
- [x] CRUD MovementGroups
- [x] CRUD Equipment (soft delete)
- [x] CRUD Exercises (soft delete) — com filtros, paginação, busca
- [x] CRUD ExerciseInstructions (aninhado sob exercises)
- [x] CRUD ExerciseAlternatives (aninhado sob exercises)
- [x] Equipment associável no create/update de Exercise (`equipment_ids`)
- [x] ExerciseResponse inclui `equipment`, `muscle_group`, `movement_group` (objetos aninhados)
- [x] Filtro `equipment_ids` funcional na listagem de exercises (JOIN + DISTINCT)
- [x] Rota `GET /exercises/` aceita query params: name, difficulty, search, muscle_group_ids, movement_group_ids, equipment_ids, order_by, order_dir

### Catálogo Público (`/api/v1/catalog`)
- [x] Listar exercises
- [x] Listar muscle-groups
- [x] Listar movement-groups
- [x] Listar equipment

### Mídia
- [x] Upload de imagens/vídeos (`POST /api/v1/admin/media/upload`)
- [x] Deletar mídia (`DELETE /api/v1/admin/media/{folder}/{filename}`)
- [x] Storage local (dev) com StaticFiles
- [x] Storage S3/MinIO (prod)

### Infraestrutura
- [x] Migrations Alembic (9 tabelas + users + role)
- [x] Seed script (admin user + 40 exercises)
- [x] Docker Compose (PostgreSQL + MinIO prod, SQLite dev)
- [x] Healthcheck com ping no banco
- [x] Logging configurável
- [x] Error handlers globais
- [x] CORS dinâmico

### Workouts (Treinos do Usuário) (`/api/v1/workouts`)
- [x] CRUD Workouts (scoped ao usuário logado)
- [x] Listar workouts do usuário com paginação
- [x] Adicionar/remover/atualizar exercícios no workout
- [x] Reordenar exercícios do workout
- [x] WorkoutResponse inclui `exercises` com `exercise` aninhado (ExerciseResponse completo)
- [x] Isolamento entre usuários (usuário A não vê treinos do usuário B)
- [x] Migração Alembic para tabelas `workouts` e `workout_exercises`

### Melhorias
- [x] `?include=instructions,alternatives` em GET /exercises/{id} e GET /exercises/
- [x] `UserResponse` agora inclui `updated_at`
- [x] `file_too_large()` helper + media.py usa helper uniforme
- [x] Handler global para `IntegrityError` → 409 Conflict com mensagem amigável

### Testes
- [x] 79 testes de integração (auth, catalog CRUD, role-based, mídia, users, alternatives, instructions, equipment association, nested relations, workouts, include, uniqueness)

## Appendix: Mapa de Relações do Schema

### Exercise ↔ MuscleGroup (N:1)
| Camada | Status |
|---|---|
| Model (`muscle_group_id` FK + `lazy="joined"`) | ✅ |
| `ExerciseResponse` com `muscle_group: MuscleGroupResponse` | ✅ |
| `GET /exercises/{id}` retorna muscle_group aninhado | ✅ |

### Exercise ↔ MovementGroup (N:1)
| Camada | Status |
|---|---|
| Model (`movement_group_id` FK + `lazy="joined"`) | ✅ |
| `ExerciseResponse` com `movement_group: MovementGroupResponse` | ✅ |
| `GET /exercises/` retorna movement_group aninhado | ✅ |

### Exercise ↔ Equipment (M:N via `exercise_equipments`)
| Camada | Status |
|---|---|
| Model (`Exercise.equipment_relations` lazy="selectin") | ✅ |
| `ExerciseCreate` com `equipment_ids: List[UUID]` | ✅ |
| `ExerciseUpdate` com `equipment_ids: Optional[List[UUID]]` | ✅ |
| `ExerciseResponse` com `equipment: List[EquipmentResponse]` | ✅ |
| `ExerciseService.create()` persiste associações | ✅ |
| `ExerciseService.update()` sincroniza associações (diff) | ✅ |
| Filtro `equipment_ids` no `list_exercises` (JOIN + DISTINCT) | ✅ |
| `GET /exercises/` aceita `equipment_ids` query param | ✅ |

### Exercise → Instructions (1:N)
| Camada | Status |
|---|---|
| Model | ✅ |
| CRUD via rotas aninhadas | ✅ |
| `?include=instructions` inline | ⏳ Pendente |

### Exercise → Alternatives (1:N)
| Camada | Status |
|---|---|
| Model | ✅ |
| CRUD via rotas aninhadas | ✅ |
| `?include=alternatives` inline | ⏳ Pendente |

### User ↔ Exercise (N:N — treinos/séries via WorkoutExercise)
| Camada | Status |
|---|---|
| Model `Workout` (user_id FK) | ✅ |
| Model `WorkoutExercise` (workout_id FK + exercise_id FK) | ✅ |
| `WorkoutCreate`/`WorkoutUpdate` | ✅ |
| `WorkoutExerciseCreate`/`WorkoutExerciseUpdate` | ✅ |
| `WorkoutResponse` com `exercises: List[WorkoutExerciseResponse]` | ✅ |
| `WorkoutExerciseResponse` com `exercise: ExerciseResponse` aninhado | ✅ |
| CRUD completo de workouts (scoped ao user) | ✅ |
| Gerenciar exercícios no workout (add/update/remove/reorder) | ✅ |
| Isolamento entre usuários (ownership check no service) | ✅ |

## Pendente

### Funcionalidades
- [ ] Catálogo Público — buscar exercício por ID
- [ ] Reset de senha (esqueci minha senha)
- [ ] Refresh token
- [ ] Paginação unificada nos catálogos públicos
- [ ] Endpoint de estatísticas do catálogo (`GET /api/v1/catalog/stats`)

### Infraestrutura
- [ ] CI/CD (GitHub Actions)
- [ ] Rate limiting
- [ ] Cache (Redis)
- [ ] Documentação deploy production

### Melhorias
- [ ] Tratar `example` deprecation warnings do Pydantic V2
- [x] Adicionar campo `slug` nos responses de MuscleGroup, MovementGroup e Equipment
