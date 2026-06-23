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

### Testes
- [x] 61 testes de integração (auth, catalog CRUD, role-based, mídia, users, alternatives, instructions, equipment association, nested relations)

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

### User ↔ Exercise (N:N — treinos/séries)
| Camada | Status |
|---|---|
| Não existe modelo Workout/WorkoutExercise | ❌ Feature futura |

## Pendente

### Funcionalidades
- [ ] `?include=instructions,alternatives` opcional em GET /exercises/{id}
- [ ] Catálogo Público — buscar exercício por ID
- [ ] Reset de senha (esqueci minha senha)
- [ ] Refresh token
- [ ] Paginação unificada nos catálogos públicos
- [ ] Endpoint de estatísticas do catálogo (`GET /api/v1/catalog/stats`)
- [ ] Modelo Workout/Sessão de treino (User ↔ Exercise via WorkoutExercise)

### Infraestrutura
- [ ] CI/CD (GitHub Actions)
- [ ] Rate limiting
- [ ] Cache (Redis)
- [ ] Documentação deploy production

### Melhorias
- [ ] Validação de uniqueness com mensagens amigáveis
- [ ] Tratar `example` deprecation warnings do Pydantic V2
- [ ] Uniformizar respostas de erro (formato padrão)
- [ ] Adicionar timestamps faltantes nas schemas de response
