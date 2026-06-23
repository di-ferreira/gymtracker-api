# GymTracker API — TypeScript Types

Use these interfaces to type API responses in the frontend app.

---

## Enums

```typescript
type DifficultyLevel = "Beginner" | "Intermediate" | "Advanced" | "Expert";

type MediaUrlType = "THUMBNAIL" | "IMAGE" | "GIF" | "VIDEO";

type UserRole = "admin" | "user";

type MediaFolder = "exercises" | "instructions";
```

---

## Error Response (uniforme)

Every error returns:
```typescript
interface ApiError {
  error: {
    code: string;    // e.g. "NOT_FOUND", "CONFLICT", "VALIDATION_ERROR"
    message: string;
  };
}
```

HTTP codes: 400, 401, 403, 404, 409, 413, 422, 500.

---

## User

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `users.id` |
| `email` | `string` | `users.email` |
| `name` | `string` | `users.name` |
| `role` | `UserRole` | `users.role` |
| `is_active` | `boolean` | `users.is_active` |
| `created_at` | `string` (ISO 8601) | `users.created_at` |
| `updated_at` | `string` (ISO 8601) | `users.updated_at` |

```typescript
interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
```

### Auth payloads

```typescript
interface RegisterRequest {
  email: string;    // max 255 chars
  password: string; // min 8, max 128 chars
  name: string;     // max 150 chars
}

interface LoginRequest {
  email: string;
  password: string;
}

interface TokenResponse {
  access_token: string;
  token_type: "bearer";
}

interface UpdateProfileRequest {
  name?: string;
  current_password?: string;
  new_password?: string;
}

interface AdminUpdateUserRequest {
  name?: string;
  role?: UserRole;
  is_active?: boolean;
}
```

---

## MuscleGroup

**Tabela:** `muscle_groups`

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `muscle_groups.id` |
| `name` | `string` | `muscle_groups.name` |
| `slug` | `string` | `muscle_groups.slug` |
| `description` | `string \| null` | `muscle_groups.description` |
| `order_index` | `number` | `muscle_groups.order_index` |
| `created_at` | `string` (ISO 8601) | `muscle_groups.created_at` |
| `updated_at` | `string` (ISO 8601) | `muscle_groups.updated_at` |

```typescript
interface MuscleGroup {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  order_index: number;
  created_at: string;
  updated_at: string;
}
```

### Create / Update payload

```typescript
interface MuscleGroupCreate {
  name: string;
  slug?: string;         // auto-generated if omitted
  description?: string;
  order_index?: number;  // default 0
}

interface MuscleGroupUpdate {
  name?: string;
  slug?: string;
  description?: string;
  order_index?: number;
}
```

---

## MovementGroup

**Tabela:** `movement_groups`

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `movement_groups.id` |
| `name` | `string` | `movement_groups.name` |
| `slug` | `string` | `movement_groups.slug` |
| `description` | `string \| null` | `movement_groups.description` |
| `order_index` | `number` | `movement_groups.order_index` |
| `created_at` | `string` (ISO 8601) | `movement_groups.created_at` |
| `updated_at` | `string` (ISO 8601) | `movement_groups.updated_at` |

```typescript
interface MovementGroup {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  order_index: number;
  created_at: string;
  updated_at: string;
}
```

### Create / Update payload

```typescript
interface MovementGroupCreate {
  name: string;
  slug?: string;
  description?: string;
  order_index?: number;
}

interface MovementGroupUpdate {
  name?: string;
  slug?: string;
  description?: string;
  order_index?: number;
}
```

---

## Equipment

**Tabela:** `equipments`

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `equipments.id` |
| `name` | `string` | `equipments.name` |
| `slug` | `string` | `equipments.slug` |
| `description` | `string \| null` | `equipments.description` |
| `category` | `string \| null` | `equipments.category` |
| `order_index` | `number` | `equipments.order_index` |
| `deleted_at` | `string \| null` (ISO 8601) | `equipments.deleted_at` (soft delete) |
| `created_at` | `string` (ISO 8601) | `equipments.created_at` |
| `updated_at` | `string` (ISO 8601) | `equipments.updated_at` |

```typescript
interface Equipment {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  category: string | null;
  order_index: number;
  deleted_at: string | null;
  created_at: string;
  updated_at: string;
}
```

### Create / Update payload

```typescript
interface EquipmentCreate {
  name: string;
  slug?: string;
  description?: string;
  category?: string;
  order_index?: number;
}

interface EquipmentUpdate {
  name?: string;
  slug?: string;
  description?: string;
  category?: string;
  order_index?: number;
}
```

---

## Exercise

**Tabela:** `exercises`

**Response** (GET /exercises/ e GET /exercises/{id}):

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `exercises.id` |
| `name` | `string` | `exercises.name` |
| `slug` | `string` | `exercises.slug` |
| `description` | `string \| null` | `exercises.description` |
| `execution_tips` | `string \| null` | `exercises.execution_tips` |
| `difficulty` | `DifficultyLevel \| null` | `exercises.difficulty` |
| `thumbnail_url` | `string \| null` | `exercises.thumbnail_url` |
| `image_url` | `string \| null` | `exercises.image_url` |
| `gif_url` | `string \| null` | `exercises.gif_url` |
| `video_url` | `string \| null` | `exercises.video_url` |
| `movement_group_id` | `string` (uuid) | FK → `movement_groups.id` |
| `muscle_group_id` | `string` (uuid) | FK → `muscle_groups.id` |
| `muscle_group` | `MuscleGroup` | Sempre incluso (lazy: joined) |
| `movement_group` | `MovementGroup` | Sempre incluso (lazy: joined) |
| `equipment` | `Equipment[]` | Sempre incluso |
| `instructions` | `ExerciseInstruction[] \| null` | `null` se `?include=` não incluir "instructions" |
| `alternatives` | `ExerciseAlternative[] \| null` | `null` se `?include=` não incluir "alternatives" |
| `created_at` | `string` (ISO 8601) | `exercises.created_at` |
| `updated_at` | `string` (ISO 8601) | `exercises.updated_at` |

```typescript
interface ExerciseResponse {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  execution_tips: string | null;
  difficulty: DifficultyLevel | null;
  thumbnail_url: string | null;
  image_url: string | null;
  gif_url: string | null;
  video_url: string | null;
  movement_group_id: string;
  muscle_group_id: string;
  muscle_group: MuscleGroup;
  movement_group: MovementGroup;
  equipment: Equipment[];
  instructions: ExerciseInstruction[] | null;  // requires ?include=instructions
  alternatives: ExerciseAlternative[] | null;  // requires ?include=alternatives
  created_at: string;
  updated_at: string;
}

// Listagem retorna ExerciseResponse[] (com instructions/alternatives = null por padrão)
```

### Create / Update payload

```typescript
interface ExerciseCreate {
  name: string;
  description?: string;
  execution_tips?: string;
  difficulty?: DifficultyLevel;
  thumbnail_url?: string;
  image_url?: string;
  gif_url?: string;
  video_url?: string;
  movement_group_id: string;
  muscle_group_id: string;
  equipment_ids?: string[];        // UUIDs dos equipamentos
}

interface ExerciseUpdate {
  name?: string;
  slug?: string;
  description?: string;
  execution_tips?: string;
  difficulty?: DifficultyLevel;
  thumbnail_url?: string;
  image_url?: string;
  gif_url?: string;
  video_url?: string;
  equipment_ids?: string[] | null; // null = não alterar, [] = limpar
}
```

### Parâmetros de filtro (GET /exercises/)

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `skip` | `number` | Offset (paginacão) |
| `limit` | `number` | Limite por página (max 100) |
| `name` | `string` | Filtro por nome (ILike) |
| `difficulty` | `DifficultyLevel` | Filtro exato |
| `search` | `string` | Busca em name + slug |
| `muscle_group_ids` | `string[]` | UUIDs |
| `movement_group_ids` | `string[]` | UUIDs |
| `equipment_ids` | `string[]` | UUIDs (JOIN + DISTINCT) |
| `include` | `string` | `"instructions,alternatives"` (separados por vírgula) |
| `order_by` | `string` | Campo de ordenacão (default: "name") |
| `order_dir` | `string` | `"asc"` ou `"desc"` (default: "asc") |

---

## ExerciseInstruction

**Tabela:** `exercise_instructions`

**Rotas:** `GET/POST /exercises/{id}/instructions/`, `PATCH/DELETE /exercises/{id}/instructions/{instr_id}`

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `exercise_instructions.id` |
| `exercise_id` | `string` (uuid) | FK → `exercises.id` |
| `step_order` | `number` | `exercise_instructions.step_order` |
| `description` | `string` | `exercise_instructions.description` |
| `image_url` | `string \| null` | `exercise_instructions.image_url` |
| `created_at` | `string` (ISO 8601) | `exercise_instructions.created_at` |
| `updated_at` | `string` (ISO 8601) | `exercise_instructions.updated_at` |

```typescript
interface ExerciseInstruction {
  id: string;
  exercise_id: string;
  step_order: number;
  description: string;
  image_url: string | null;
  created_at: string;
  updated_at: string;
}

interface InstructionCreate {
  description: string;
  step_order?: number;
  image_url?: string;
}

interface InstructionUpdate {
  description?: string;
  step_order?: number;
  image_url?: string;
}
```

---

## ExerciseAlternative

**Tabela:** `exercise_alternatives`

**Rotas:** `GET/POST /exercises/{id}/alternatives/`, `DELETE /exercises/{id}/alternatives/{alt_id}`

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `exercise_alternatives.id` |
| `exercise_id` | `string` (uuid) | FK → `exercises.id` |
| `alternative_exercise_id` | `string` (uuid) | FK → `exercises.id` |
| `reason` | `string \| null` | `exercise_alternatives.reason` |
| `note` | `string \| null` | `exercise_alternatives.note` |
| `created_at` | `string` (ISO 8601) | `exercise_alternatives.created_at` |
| `updated_at` | `string` (ISO 8601) | `exercise_alternatives.updated_at` |

```typescript
interface ExerciseAlternative {
  id: string;
  exercise_id: string;
  alternative_exercise_id: string;
  reason: string | null;
  note: string | null;
  created_at: string;
  updated_at: string;
}

interface AlternativeCreate {
  alternative_exercise_id: string;
  reason?: string;
  note?: string;
}
```

---

## Workout

**Tabela:** `workouts`

**Rotas:** Autenticadas em `/api/v1/workouts/`

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `workouts.id` |
| `user_id` | `string` (uuid) | FK → `users.id` |
| `name` | `string` | `workouts.name` |
| `notes` | `string \| null` | `workouts.notes` |
| `exercises` | `WorkoutExercise[]` | Relacionamento (lazy: selectin) |
| `created_at` | `string` (ISO 8601) | `workouts.created_at` |
| `updated_at` | `string` (ISO 8601) | `workouts.updated_at` |

```typescript
interface Workout {
  id: string;
  user_id: string;
  name: string;
  notes: string | null;
  exercises: WorkoutExercise[];
  created_at: string;
  updated_at: string;
}

interface WorkoutCreate {
  name: string;
  notes?: string;
}

interface WorkoutUpdate {
  name?: string;
  notes?: string;
}
```

---

## WorkoutExercise

**Tabela:** `workout_exercises`

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `workout_exercises.id` |
| `workout_id` | `string` (uuid) | FK → `workouts.id` |
| `exercise_id` | `string` (uuid) | FK → `exercises.id` |
| `exercise` | `ExerciseResponse` | Sempre incluso (lazy: joined) |
| `sort_order` | `number` | `workout_exercises.sort_order` |
| `sets` | `number \| null` | `workout_exercises.sets` |
| `reps` | `number \| null` | `workout_exercises.reps` |
| `weight` | `number \| null` | `workout_exercises.weight` |
| `notes` | `string \| null` | `workout_exercises.notes` |
| `created_at` | `string` (ISO 8601) | `workout_exercises.created_at` |
| `updated_at` | `string` (ISO 8601) | `workout_exercises.updated_at` |

```typescript
interface WorkoutExercise {
  id: string;
  workout_id: string;
  exercise_id: string;
  exercise: ExerciseResponse;
  sort_order: number;
  sets: number | null;
  reps: number | null;
  weight: number | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

interface WorkoutExerciseCreate {
  exercise_id: string;
  sort_order?: number;
  sets?: number;
  reps?: number;
  weight?: number;
  notes?: string;
}

interface WorkoutExerciseUpdate {
  sort_order?: number;
  sets?: number;
  reps?: number;
  weight?: number;
  notes?: string;
}

interface WorkoutReorder {
  exercise_ids: string[];  // ordered list of WorkoutExercise IDs
}
```

---

## ExerciseEquipment (join table)

**Tabela:** `exercise_equipments`

Usada internamente. No response do Exercise, os equipamentos aparecem como `Equipment[]` no campo `equipment`.

| Campo | Tipo | Origem |
|---|---|---|
| `exercise_id` | `string` (uuid) | FK → `exercises.id` (PK composta) |
| `equipment_id` | `string` (uuid) | FK → `equipments.id` (PK composta) |
| `usage_note` | `string \| null` | `exercise_equipments.usage_note` |

```typescript
interface ExerciseEquipment {
  exercise_id: string;
  equipment_id: string;
  usage_note: string | null;
}
```

---

## CatalogVersion

**Tabela:** `catalog_versions`

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `catalog_versions.id` |
| `version_major` | `number` | `catalog_versions.version_major` |
| `version_minor` | `number` | `catalog_versions.version_minor` |
| `checksum` | `string` | `catalog_versions.checksum` |
| `status` | `string` | `catalog_versions.status` |
| `description` | `string \| null` | `catalog_versions.description` |
| `checksum_algorithm` | `string` | `catalog_versions.checksum_algorithm` |
| `sync_metadata` | `string \| null` | `catalog_versions.sync_metadata` |
| `created_at` | `string` (ISO 8601) | `catalog_versions.created_at` |
| `updated_at` | `string` (ISO 8601) | `catalog_versions.updated_at` |

```typescript
interface CatalogVersion {
  id: string;
  version_major: number;
  version_minor: number;
  checksum: string;
  status: string;
  description: string | null;
  checksum_algorithm: string;
  sync_metadata: string | null;
  created_at: string;
  updated_at: string;
}
```

---

## Media

```typescript
interface MediaUploadResponse {
  url: string;
  path: string;       // e.g. "exercises/uuid.jpg"
  filename: string;
}

interface MediaDeleteResponse {
  deleted: true;
}
```

---

## API mapeamento de rotas

### Autenticação

| Rota | Tipo de resposta |
|---|---|
| `POST /api/v1/auth/register` | `User` |
| `POST /api/v1/auth/login` | `TokenResponse` |
| `GET /api/v1/auth/me` | `User` |
| `PATCH /api/v1/auth/me` | `User` |

### Catálogo Público (`/api/v1/catalog`)

| Rota | Tipo de resposta |
|---|---|
| `GET /api/v1/catalog/exercises/` | `ExerciseResponse[]` |
| `GET /api/v1/catalog/muscle-groups/` | `MuscleGroup[]` |
| `GET /api/v1/catalog/movement-groups/` | `MovementGroup[]` |
| `GET /api/v1/catalog/equipment/` | `Equipment[]` |

### Admin — Catálogo (`/api/v1/admin/catalog`)

| Rota | Tipo de resposta |
|---|---|
| `GET /exercises/` | `ExerciseResponse[]` (com filtros) |
| `POST /exercises/` | `ExerciseResponse` |
| `GET /exercises/{id}` | `ExerciseResponse` (com `?include=`) |
| `PATCH /exercises/{id}` | `ExerciseResponse` |
| `DELETE /exercises/{id}` | `204 No Content` |
| `GET /exercises/{id}/instructions/` | `ExerciseInstruction[]` |
| `POST /exercises/{id}/instructions/` | `ExerciseInstruction` |
| `PATCH /exercises/{id}/instructions/{instr_id}` | `ExerciseInstruction` |
| `DELETE /exercises/{id}/instructions/{instr_id}` | `204 No Content` |
| `GET /exercises/{id}/alternatives/` | `ExerciseAlternative[]` |
| `POST /exercises/{id}/alternatives/` | `ExerciseAlternative` |
| `DELETE /exercises/{id}/alternatives/{alt_id}` | `204 No Content` |
| CRUD `/muscle-groups/`, `/movement-groups/`, `/equipment/` | Entidade correspondente |

### Admin — Usuários (`/api/v1/admin`)

| Rota | Tipo de resposta |
|---|---|
| `GET /admin/users/` | `User[]` |
| `PATCH /admin/users/{id}` | `User` |

### Admin — Mídia (`/api/v1/admin/media`)

| Rota | Tipo de resposta |
|---|---|
| `POST /admin/media/upload` | `MediaUploadResponse` |
| `DELETE /admin/media/{folder}/{filename}` | `MediaDeleteResponse` |

### Workouts (`/api/v1/workouts` — autenticado)

| Rota | Tipo de resposta |
|---|---|
| `GET /workouts/` | `Workout[]` |
| `POST /workouts/` | `Workout` |
| `GET /workouts/{id}` | `Workout` |
| `PATCH /workouts/{id}` | `Workout` |
| `DELETE /workouts/{id}` | `204 No Content` |
| `POST /workouts/{id}/exercises/` | `WorkoutExercise` |
| `PATCH /workouts/{id}/exercises/{we_id}` | `WorkoutExercise` |
| `DELETE /workouts/{id}/exercises/{we_id}` | `204 No Content` |
| `PUT /workouts/{id}/exercises/reorder` | `{ status: "ok" }` |
