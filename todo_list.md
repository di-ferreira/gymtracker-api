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
- [x] Gerenciamento equipment relations no Exercise

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
- [x] 57 testes de integração (auth, catalog CRUD, role-based, mídia, users, alternatives, instructions)

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
- [ ] Validação de uniqueness com mensagens amigáveis
- [ ] Tratar `example` deprecation warnings do Pydantic V2
- [ ] Uniformizar respostas de erro (formato padrão)
- [ ] Adicionar timestamps faltantes nas schemas de response
