# GymTracker API — TypeScript Types

Use these interfaces to type API responses in the frontend app.

---

## Enums

```typescript
type DifficultyLevel = "Beginner" | "Intermediate" | "Advanced" | "Expert";

type MediaUrlType = "THUMBNAIL" | "IMAGE" | "GIF" | "VIDEO";

type UserRole = "admin" | "user";
```

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

| Campo | Tipo | Origem |
|---|---|---|
| `id` | `string` (uuid) | `exercises.id` |
| `name` | `string` | `exercises.name` |
| `slug` | `string` | `exercises.slug` |
| `description` | `string \| null` | `exercises.description` |
| `execution_tips` | `string \| null` | `exercises.execution_tips` |
| `difficulty` | `DifficultyLevel \| null` | `exercises.difficulty` |
| `target_muscle_primary` | `string \| null` | `exercises.target_muscle_primary` |
| `thumbnail_url` | `string \| null` | `exercises.thumbnail_url` |
| `image_url` | `string \| null` | `exercises.image_url` |
| `gif_url` | `string \| null` | `exercises.gif_url` |
| `video_url` | `string \| null` | `exercises.video_url` |
| `movement_group_id` | `string` (uuid) | FK → `movement_groups.id` |
| `muscle_group_id` | `string` (uuid) | FK → `muscle_groups.id` |
| `movement_group` | `MovementGroup` | Relacionamento (lazy: joined) |
| `muscle_group` | `MuscleGroup` | Relacionamento (lazy: joined) |
| `equipment_relations` | `ExerciseEquipment[]` | Relacionamento (lazy: selectin) |
| `instructions` | `ExerciseInstruction[]` | Relacionamento (lazy: selectin) |
| `alternatives` | `ExerciseAlternative[]` | Relacionamento (lazy: selectin) |
| `deleted_at` | `string \| null` (ISO 8601) | `exercises.deleted_at` (soft delete) |
| `created_at` | `string` (ISO 8601) | `exercises.created_at` |
| `updated_at` | `string` (ISO 8601) | `exercises.updated_at` |

```typescript
interface Exercise {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  execution_tips: string | null;
  difficulty: DifficultyLevel | null;
  target_muscle_primary: string | null;
  thumbnail_url: string | null;
  image_url: string | null;
  gif_url: string | null;
  video_url: string | null;
  movement_group_id: string;
  muscle_group_id: string;
  movement_group: MovementGroup;
  muscle_group: MuscleGroup;
  equipment_relations: ExerciseEquipment[];
  instructions: ExerciseInstruction[];
  alternatives: ExerciseAlternative[];
  deleted_at: string | null;
  created_at: string;
  updated_at: string;
}
```

### Create / Update payload

```typescript
interface ExerciseCreate {
  name: string;
  slug?: string;
  description?: string;
  execution_tips?: string;
  difficulty?: DifficultyLevel;
  target_muscle_primary?: string;
  thumbnail_url?: string;
  image_url?: string;
  gif_url?: string;
  video_url?: string;
  movement_group_id: string;
  muscle_group_id: string;
}

interface ExerciseUpdate {
  name?: string;
  slug?: string;
  description?: string;
  execution_tips?: string;
  difficulty?: DifficultyLevel;
  target_muscle_primary?: string;
  thumbnail_url?: string;
  image_url?: string;
  gif_url?: string;
  video_url?: string;
  movement_group_id?: string;
  muscle_group_id?: string;
}
```

---

## ExerciseEquipment

**Tabela:** `exercise_equipments`

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

## ExerciseInstruction

**Tabela:** `exercise_instructions`

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
```

---

## ExerciseAlternative

**Tabela:** `exercise_alternatives`

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

## API mapeamento de rotas

| Rota | Tipo de resposta |
|---|---|
| `POST /api/v1/auth/register` | `User` |
| `POST /api/v1/auth/login` | `TokenResponse` |
| `GET /api/v1/auth/me` | `User` |
| `PATCH /api/v1/auth/me` | `User` |
| `GET /api/v1/catalog/exercises/` | `Exercise[]` |
| `GET /api/v1/catalog/muscle-groups/` | `MuscleGroup[]` |
| `GET /api/v1/catalog/movement-groups/` | `MovementGroup[]` |
| `GET /api/v1/catalog/equipment/` | `Equipment[]` |
| `GET /api/v1/admin/users/` | `User[]` |
| `PATCH /api/v1/admin/users/{id}` | `User` |
| Todas as rotas `POST /api/v1/admin/catalog/*` | Entidade correspondente |
| Todas as rotas `GET /api/v1/admin/catalog/*` | Entidade correspondente ou `Entity[]` |
| Todas as rotas `PATCH /api/v1/admin/catalog/*` | Entidade correspondente |
| Todas as rotas `DELETE /api/v1/admin/catalog/*` | `204 No Content` |
