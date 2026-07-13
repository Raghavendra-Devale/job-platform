# Job Platform — API Documentation

> **Generated**: 2026-07-13  
> **Repos Covered**: `job-platform-api` (Spring Boot), `fastapi-ai` (Python AI Engine), `job-platform-ui` (Angular Frontend)

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [job-platform-api — Spring Boot REST APIs](#job-platform-api--spring-boot-rest-apis)
   - [Authentication](#1-authentication-apiauth)
   - [User Profile](#2-user-profile-apiusersprofile)
   - [Resume Management](#3-resume-management-apiusersprofileresumes)
   - [Jobs](#4-jobs-apijobs)
   - [Job Providers](#5-job-providers-apiproviders)
   - [Saved Jobs](#6-saved-jobs)
   - [Recently Viewed Jobs](#7-recently-viewed-jobs)
   - [Dashboard](#8-dashboard-apidashboard)
   - [Recommendations](#9-recommendations-apirecommendations)
3. [fastapi-ai — Python AI Engine APIs](#fastapi-ai--python-ai-engine-apis)
   - [Root Health](#1-root-health)
   - [AI Health](#2-ai-health-apiv1health)
   - [Resume Processing](#3-resume-processing-apiv1resumeprocess)
   - [Job Processing](#4-job-processing-apiv1jobprocess)
   - [Recommendations Generation](#5-recommendations-generation-apiv1recommendationsgenerate)
4. [job-platform-ui — Angular Frontend Routes](#job-platform-ui--angular-frontend-routes)
5. [Error Response Formats](#error-response-formats)
6. [Data Models Reference](#data-models-reference)

---

## Architecture Overview

```
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│   job-platform-ui   │◄────►│  job-platform-api   │◄────►│     fastapi-ai      │
│   (Angular 19)      │      │  (Spring Boot)      │      │  (FastAPI + LLM)    │
│   Port: 4200        │      │  Port: 8080         │      │  Port: 8000         │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
                                      │                            │
                                      ▼                            ▼
                              ┌───────────────┐           ┌───────────────┐
                              │  PostgreSQL   │           │  PostgreSQL   │
                              │  (public)     │           │  (ai schema)  │
                              └───────────────┘           └───────────────┘
```

- **job-platform-api**: Core business API — users, authentication (JWT + HttpOnly cookies), jobs (CRUD, search, sync from external providers), resumes, applications, dashboard, and recommendations orchestration.
- **fastapi-ai**: AI microservice — processes resumes (PDF → structured extraction via LLM), processes job descriptions (normalization + LLM analysis), generates vector embeddings, persists to `ai.*` PostgreSQL schema, and runs multi-dimensional recommendation scoring.
- **job-platform-ui**: Angular 19 SPA consuming the Spring Boot APIs via a dev proxy.

---

## job-platform-api — Spring Boot REST APIs

**Base URL**: `http://localhost:8080`  
**Auth**: JWT via HttpOnly cookie (`jwt`) or `Authorization: Bearer <token>` header.

---

### 1. Authentication (`/api/auth`)

#### `POST /api/auth/register`
Register a new user account.

| Field      | Type   | Required | Validation                        |
|------------|--------|----------|-----------------------------------|
| `name`     | string | ✅       | 2–50 characters                   |
| `email`    | string | ✅       | Valid email format                 |
| `password` | string | ✅       | Minimum 6 characters              |

**Success Response** `201 Created`:
```json
{ "message": "User registered successfully" }
```

**Error Response** `400 Bad Request`:
```json
{ "error": "Email is already in use" }
```

---

#### `POST /api/auth/login`
Authenticate and receive a JWT token. Sets an HttpOnly cookie for session security.

| Field      | Type   | Required |
|------------|--------|----------|
| `email`    | string | ✅       |
| `password` | string | ✅       |

**Success Response** `200 OK`:
```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "USER"
}
```
**Headers**: `Set-Cookie: jwt=<token>; HttpOnly; Path=/; Max-Age=86400; SameSite=Strict`

---

#### `POST /api/auth/logout`
Clear the authentication session by expiring the HttpOnly cookie.

**Success Response** `200 OK`:
```json
{ "message": "Logged out successfully" }
```

---

### 2. User Profile (`/api/users/profile`)

> 🔒 **Auth Required** — All endpoints below require authentication.

#### `GET /api/users/profile`
Get the authenticated user's complete profile, including profile details and preferences.

**Response** `200 OK`:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "USER",
  "resumeFileName": "john_resume.pdf",
  "workPreference": "REMOTE",
  "alertEnabled": true,
  "createdAt": "2026-01-01T00:00:00",
  "experience": 5,
  "currentRole": "Software Engineer",
  "bio": "Passionate developer...",
  "linkedin": "https://linkedin.com/in/johndoe",
  "github": "https://github.com/johndoe",
  "portfolio": "https://johndoe.dev",
  "phone": "+1-555-0100",
  "location": "San Francisco, CA",
  "preferredRoles": "Backend Engineer, Full Stack",
  "preferredLocations": "San Francisco, Remote",
  "remoteOnly": false,
  "salaryRange": "$120k-$180k",
  "jobTypes": "Full-time"
}
```

---

#### `PUT /api/users/profile`
Update the user's profile information.

| Field         | Type    | Required | Validation                  |
|---------------|---------|----------|-----------------------------|
| `name`        | string  | ✅       | 2–50 characters             |
| `email`       | string  | ✅       | Valid email                  |
| `experience`  | integer | ❌       | ≥ 0                         |
| `currentRole` | string  | ❌       |                             |
| `bio`         | string  | ❌       |                             |
| `linkedin`    | string  | ❌       |                             |
| `github`      | string  | ❌       |                             |
| `portfolio`   | string  | ❌       |                             |
| `phone`       | string  | ❌       |                             |
| `location`    | string  | ❌       |                             |

**Success Response** `200 OK`:
```json
{ "message": "Profile updated successfully" }
```

---

#### `POST /api/users/profile/change-password`
Change the authenticated user's password.

| Field             | Type   | Required | Validation               |
|-------------------|--------|----------|--------------------------|
| `currentPassword` | string | ✅       |                          |
| `newPassword`     | string | ✅       | Minimum 6 characters     |

**Success** `200 OK`: `{ "message": "Password changed successfully" }`  
**Error** `400`: `{ "error": "Incorrect current password" }`

---

#### `PUT /api/users/profile/preferences`
Update the user's job search preferences.

| Field               | Type    | Required |
|---------------------|---------|----------|
| `workPreference`    | string  | ✅       |
| `alertEnabled`      | boolean | ✅       |
| `preferredRoles`    | string  | ❌       |
| `preferredLocations`| string  | ❌       |
| `remoteOnly`        | boolean | ❌       |
| `salaryRange`       | string  | ❌       |
| `jobTypes`          | string  | ❌       |

**Success** `200 OK`: `{ "message": "Preferences updated successfully" }`

---

### 3. Resume Management (`/api/users/profile/resumes`)

> 🔒 **Auth Required**

#### `GET /api/users/profile/resumes`
List all resumes for the authenticated user (ordered by most recently updated).

**Response** `200 OK`:
```json
[
  {
    "id": 1,
    "resumeName": "my_resume.pdf",
    "active": true,
    "updatedAt": "2026-07-01T10:30:00"
  }
]
```

---

#### `POST /api/users/profile/resumes`
Upload a new resume file.

| Field  | Type          | Required | Content-Type               |
|--------|---------------|----------|----------------------------|
| `file` | MultipartFile | ✅       | `multipart/form-data`      |

**Success** `201 Created`: Returns `ResumeResponse`.

---

#### `PUT /api/users/profile/resumes/{id}/activate`
Set a specific resume as the active resume.

**Success** `200 OK`: `{ "message": "Resume activated successfully" }`

---

#### `PUT /api/users/profile/resumes/{id}/rename`
Rename a resume.

| Field        | Type   | Required |
|--------------|--------|----------|
| `resumeName` | string | ✅       |

**Success** `200 OK`: Returns updated `ResumeResponse`.

---

#### `DELETE /api/users/profile/resumes/{id}`
Delete a resume.

**Success** `200 OK`: `{ "message": "Resume deleted successfully" }`

---

#### `GET /api/users/profile/resumes/{id}/download`
Download the resume file. Returns binary content with appropriate `Content-Type` header (PDF, DOC, DOCX).

---

### 4. Jobs (`/api/jobs`)

#### `GET /api/jobs`
Get a paginated list of all jobs.

| Param  | Type | Default | Description        |
|--------|------|---------|--------------------|
| `page` | int  | 0       | Page number        |
| `size` | int  | 10      | Items per page     |

**Response** `200 OK`: Spring `Page<JobListResponse>`.

```json
{
  "content": [
    {
      "id": 1,
      "title": "Backend Developer",
      "company": "Acme Corp",
      "location": "Remote",
      "source": "RemoteOK",
      "remote": true,
      "tags": "python,fastapi",
      "createdAt": "2026-07-01T12:00:00",
      "salary": "$120k",
      "jobType": "Full-time",
      "applyUrl": "https://example.com/apply"
    }
  ],
  "totalElements": 150,
  "totalPages": 15,
  "size": 10,
  "number": 0,
  "first": true,
  "last": false,
  "empty": false
}
```

---

#### `GET /api/jobs/search`
Search jobs with filters, keyword weighting, sorting, and pagination.

| Param           | Type    | Description                              |
|-----------------|---------|------------------------------------------|
| `keyword`       | string  | Search keyword for title/description     |
| `location`      | string  | Filter by location                       |
| `remote`        | boolean | Filter remote jobs only                  |
| `salaryMin`     | string  | Minimum salary filter                    |
| `salaryMax`     | string  | Maximum salary filter                    |
| `page`          | int     | Page number                              |
| `size`          | int     | Items per page                           |
| `sortBy`        | string  | Sort field                               |
| `sortDirection` | string  | `ASC` or `DESC`                          |
| `provider`      | string  | Filter by job source provider            |
| `experience`    | string  | Filter by experience level               |
| `jobType`       | string  | Filter by job type                       |
| `company`       | string  | Filter by company name                   |

**Response** `200 OK`:
```json
{
  "content": [ ... ],
  "filters": {
    "locations": ["Remote", "New York"],
    "companies": ["Google", "Meta"]
  },
  "totalElements": 50,
  "totalPages": 5,
  "size": 10,
  "number": 0
}
```

---

#### `GET /api/jobs/{id}`
Get detailed information for a single job. Automatically records a recent view if the user is authenticated.

**Response** `200 OK`:
```json
{
  "slug": "backend-developer-acme",
  "title": "Backend Developer",
  "company": "Acme Corp",
  "location": "Remote",
  "description": "Full job description HTML...",
  "applyUrl": "https://example.com/apply",
  "remote": true,
  "tags": "python,fastapi,docker"
}
```

---

#### `POST /api/jobs/sync`
Trigger a manual synchronization of jobs from all configured external providers.

**Response** `200 OK`:
```json
{
  "providers": [
    { "provider": "RemoteOK", "fetched": 100, "inserted": 25, "skipped": 75 }
  ]
}
```

---

### 5. Job Providers (`/api/providers`)

#### `GET /api/providers/health`
Check health status of all configured external job providers.

**Response** `200 OK`:
```json
{ "RemoteOK": "UP", "Arbeitnow": "DOWN" }
```

---

#### `GET /api/providers/search?keyword={keyword}`
Live search against external provider APIs.

**Response** `200 OK`: `JobResponse[]`

---

### 6. Saved Jobs

> 🔒 **Auth Required**

#### `POST /api/jobs/{jobId}/save`
Save a job to the user's bookmarks.

**Success** `201 Created`: `{ "message": "Job saved successfully" }`

---

#### `DELETE /api/jobs/{jobId}/save`
Remove a job from the user's bookmarks.

**Success** `200 OK`: `{ "message": "Job unsaved successfully" }`

---

#### `GET /api/jobs/saved`
Get all saved jobs for the authenticated user.

**Response** `200 OK`: `JobListResponse[]`

---

#### `GET /api/jobs/saved/ids`
Get IDs of all saved jobs (lightweight endpoint for UI bookmark state).

**Response** `200 OK`: `[1, 5, 12, 43]`

---

### 7. Recently Viewed Jobs

> 🔒 **Auth Required**

#### `POST /api/jobs/{jobId}/view`
Record a job view event for the authenticated user.

**Success** `200 OK`: `{ "message": "Job view recorded" }`

---

#### `GET /api/jobs/recent`
Get the 10 most recently viewed jobs for the authenticated user.

**Response** `200 OK`: `JobListResponse[]`

---

### 8. Dashboard (`/api/dashboard`)

> 🔒 **Auth Required**

#### `GET /api/dashboard/summary`
Get the dashboard summary with counts and recent activity.

**Response** `200 OK`:
```json
{
  "activeResumeName": "my_resume.pdf",
  "totalResumesCount": 3,
  "savedJobsCount": 12,
  "applicationsCount": 5,
  "interviewsCount": 2,
  "offersCount": 1,
  "recentActivities": [
    {
      "id": 1,
      "activityType": "JOB_SAVED",
      "description": "Saved job 'Backend Dev at Google'",
      "createdAt": "2026-07-10T14:00:00"
    }
  ]
}
```

---

#### `GET /api/dashboard/applications`
List all job applications for the authenticated user.

**Response** `200 OK`:
```json
[
  {
    "id": 1,
    "jobId": 42,
    "jobTitle": "Backend Developer",
    "company": "Google",
    "location": "Mountain View",
    "status": "INTERVIEW",
    "appliedAt": "2026-06-15T10:00:00",
    "updatedAt": "2026-07-01T14:00:00",
    "resumeName": "my_resume.pdf"
  }
]
```

---

#### `POST /api/dashboard/applications`
Create a new job application tracker entry. Automatically attaches the active resume.

| Field   | Type | Required |
|---------|------|----------|
| `jobId` | Long | ✅       |

**Success** `201 Created`: Returns `JobApplicationResponse`.

---

#### `PUT /api/dashboard/applications/{id}/status`
Update the status of a job application.

| Field    | Type   | Required | Valid Values                                     |
|----------|--------|----------|--------------------------------------------------|
| `status` | string | ✅       | `APPLIED`, `SCREENING`, `INTERVIEW`, `OFFER`, `REJECTED` |

**Success** `200 OK`: `{ "message": "Application status updated successfully" }`

---

#### `DELETE /api/dashboard/applications/{id}`
Delete a job application tracker entry.

**Success** `200 OK`: `{ "message": "Application tracker deleted successfully" }`

---

### 9. Recommendations (`/api/recommendations`)

> 🔒 **Auth Required**

#### `POST /api/recommendations`
Generate AI-powered job recommendations for the authenticated user.

**Request Body** (optional):
```json
{
  "preferredRoles": ["Backend Engineer"],
  "preferredLocations": ["Remote"],
  "remoteOnly": true
}
```

**Response** `200 OK`: `RecommendationResponse` (returned from AI Engine).

---

## fastapi-ai — Python AI Engine APIs

**Base URL**: `http://localhost:8000`  
**Auth**: None (internal service-to-service communication)  
**Prefix**: All business endpoints under `/api/v1`

---

### 1. Root Health

#### `GET /`
Basic service health check.

**Response** `200 OK`:
```json
{
  "service": "FastAPI AI Engine",
  "version": "1.0.0",
  "environment": "development",
  "status": "UP"
}
```

---

### 2. AI Health (`/api/v1/health`)

#### `GET /api/v1/health`
Detailed operational health check including provider status.

**Response** `200 OK`:
```json
{
  "status": "UP",
  "embeddingProvider": "SentenceTransformerProvider",
  "llmProvider": "OllamaProvider",
  "version": "1.0.0"
}
```

---

### 3. Resume Processing (`/api/v1/resume/process`)

#### `POST /api/v1/resume/process`
Upload a PDF resume for AI-powered extraction, analysis, embedding, and persistence.

**Content-Type**: `multipart/form-data`

| Field       | Type         | Required | Description                                |
|-------------|--------------|----------|--------------------------------------------|
| `file`      | UploadFile   | ✅       | Resume PDF file (max 10 MB)                |
| `resumeId`  | int          | ❌       | Spring Boot resume entity ID (camelCase)   |
| `resume_id` | int          | ❌       | Spring Boot resume entity ID (snake_case)  |
| `userId`    | int          | ❌       | Spring Boot user entity ID (camelCase)     |
| `user_id`   | int          | ❌       | Spring Boot user entity ID (snake_case)    |

> Both camelCase and snake_case parameter names are accepted for cross-framework compatibility.

**Pipeline Steps**:
1. **Extract** — PDF text extraction via `pdfplumber`
2. **Clean** — Normalize whitespace, strip artifacts
3. **Analyze** — LLM-powered structured extraction → `CandidateProfile`
4. **Embed** — Generate 384-dim vector embedding (`all-MiniLM-L6-v2`)
5. **Suggest** — Generate resume improvement suggestions
6. **Persist** — Upsert to `ai.candidate_profiles` table

**Success Response** `200 OK`:
```json
{
  "extracted_text": "John Doe\nSoftware Engineer\n...",
  "summary": "Experienced software engineer with Python expertise...",
  "skills": [
    { "name": "Python", "confidence": 0.95 },
    { "name": "FastAPI", "confidence": 0.90 }
  ],
  "education": [
    {
      "degree": "B.S. Computer Science",
      "institution": "MIT",
      "start_date": "2018-09",
      "end_date": "2022-06"
    }
  ],
  "experience": [
    {
      "company": "Google",
      "designation": "Software Engineer",
      "start_date": "2022-07",
      "end_date": "Present",
      "responsibilities": ["Developed backend APIs", "Led code reviews"]
    }
  ],
  "certifications": [
    { "name": "AWS Solutions Architect", "issuer": "Amazon" }
  ],
  "projects": [
    {
      "name": "AI Resume Parser",
      "description": "Built an AI-powered resume parsing system",
      "technologies": ["Python", "FastAPI", "LangChain"]
    }
  ],
  "languages": [
    { "name": "English", "proficiency": "Native" }
  ]
}
```

**Error Responses**:

| Code | Description                                                 |
|------|-------------------------------------------------------------|
| 400  | Validation error (non-PDF, empty file, oversized file)      |
| 500  | Internal server error during pipeline processing            |
| 502  | AI provider or connection error                             |

---

### 4. Job Processing (`/api/v1/job/process`)

#### `POST /api/v1/job/process`
Process and persist a raw job posting through AI analysis.

**Content-Type**: `application/json`

| Field             | Type   | Required | Description                        |
|-------------------|--------|----------|------------------------------------|
| `job_id`          | int    | ✅       | Spring Boot job entity ID          |
| `title`           | string | ✅       | Raw job title                      |
| `company`         | string | ✅       | Raw company name                   |
| `location`        | string | ❌       | Raw location                       |
| `description`     | string | ❌       | Raw job description                |
| `apply_url`       | string | ❌       | Application URL                    |
| `salary`          | string | ❌       | Raw salary information             |
| `employment_type` | string | ❌       | Raw employment type                |
| `source`          | string | ❌       | External provider name             |

**Pipeline Steps**:
1. **Normalize** — Standardize text, location, employment type
2. **Analyze** — LLM-powered structured extraction → `JobProfile`
3. **Embed** — Generate 384-dim vector embedding
4. **Persist** — Upsert to `ai.job_profiles` table

**Success Response** `200 OK`:
```json
{
  "job_id": 42,
  "job_profile_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED"
}
```

---

### 5. Recommendations Generation (`/api/v1/recommendations/generate`)

#### `POST /api/v1/recommendations/generate`
Generate ranked job recommendations for a stored candidate profile.

**Content-Type**: `application/json`

| Field                  | Type   | Required | Description                          |
|------------------------|--------|----------|--------------------------------------|
| `candidate_profile_id` | string | ✅       | UUID of the stored candidate profile |

**Pipeline Steps**:
1. **Retrieve Candidate** — Load candidate profile + embedding from DB
2. **Retrieve Jobs** — Vector similarity search (top 200) or all active jobs
3. **Rank** — Multi-dimensional scoring:
   - Semantic similarity (cosine similarity of embeddings)
   - Skill match (required + preferred overlap)
   - Experience match (years comparison)
   - Location match (remote-friendly heuristic)
   - Education match (degree level comparison)
4. **Generate Reasons** — LLM-powered explanations for top matches
5. **Persist** — Log recommendation results

**Success Response** `200 OK`:
```json
{
  "recommendations": [
    {
      "title": "Senior Backend Engineer",
      "company": "TechCorp",
      "location": "Remote",
      "description": "Lead backend architecture...",
      "employment_type": "Full-time",
      "apply_url": "https://techcorp.com/apply",
      "similarity_score": 0.92,
      "recommendation_reason": "Strong match: Your Python/FastAPI skills align with 85% of required skills. Your 5 years of experience exceeds the 3+ year requirement."
    }
  ]
}
```

---

## job-platform-ui — Angular Frontend Routes

| Route              | Component               | Auth Guard | Description                         |
|--------------------|-------------------------|------------|-------------------------------------|
| `/`                | Redirect → `/jobs`      | ❌         | Home page redirect                  |
| `/jobs`            | `JobsComponent`         | ❌         | Browse and search jobs              |
| `/jobs/:id`        | `JobDetailComponent`    | ❌         | Single job detail view              |
| `/login`           | `LoginComponent`        | Guest only | Login page                          |
| `/register`        | `RegisterComponent`     | Guest only | Registration page                   |
| `/profile`         | `UserProfileComponent`  | ✅         | User profile management             |
| `/dashboard`       | `DashboardComponent`    | ✅         | Dashboard with stats & applications |
| `/saved-jobs`      | `SavedJobsComponent`    | ✅         | Bookmarked jobs list                |
| `/resumes`         | `ResumesComponent`      | ✅         | Resume management                   |
| `/applications`    | `ApplicationsComponent` | ✅         | Job application tracker             |
| `/recommendations` | `RecommendationsComponent` | ✅     | AI-powered job recommendations      |
| `/settings`        | `SettingsComponent`     | ✅         | User settings                       |
| `/admin`           | `AdminComponent`        | ❌         | Admin panel                         |
| `**`               | Redirect → `/jobs`      | ❌         | Wildcard catch-all                  |

### Frontend Services

| Service                | API Endpoints Used                                       |
|------------------------|----------------------------------------------------------|
| `AuthService`          | Auth, Profile, Preferences, Resume CRUD, Saved Jobs, Recent Jobs |
| `JobService`           | Jobs listing, Search, Sync, Provider health, External search |
| `DashboardService`     | Dashboard summary, Applications CRUD                     |
| `RecommendationService`| Recommendations generation                               |
| `NotificationService`  | Client-side notifications                                |
| `ToastService`         | Client-side toast messages                               |
| `ConfirmationModalService` | Client-side confirmation dialogs                     |

---

## Error Response Formats

### Spring Boot (job-platform-api)

Standard Spring validation errors and custom `ResponseStatusException`:
```json
{ "error": "Error message describing the issue" }
```

### FastAPI AI Engine (fastapi-ai)

All errors follow a consistent envelope format with correlation IDs:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Only PDF files are accepted.",
    "correlation_id": "abc-123-def"
  }
}
```

**Error Codes**:

| Code                    | HTTP Status | Description                               |
|-------------------------|-------------|-------------------------------------------|
| `VALIDATION_ERROR`      | 400 / 422   | Input validation failure                  |
| `RESOURCE_NOT_FOUND`    | 404         | Requested entity does not exist           |
| `EXTERNAL_SERVICE_ERROR`| 502         | AI provider or downstream service failure |
| `INTERNAL_SERVER_ERROR` | 500         | Unhandled server error                    |
| `HTTP_ERROR`            | varies      | Standard HTTP error                       |
| `UNAUTHORIZED`          | 401         | Authentication required                   |
| `FORBIDDEN`             | 403         | Insufficient permissions                  |

---

## Data Models Reference

### Resume Domain Models (fastapi-ai)

| Model              | Description                                          |
|--------------------|------------------------------------------------------|
| `Skill`            | `{ name: str, confidence: float }`                   |
| `Education`        | `{ degree, institution, start_date, end_date }`      |
| `Experience`       | `{ company, designation, start_date, end_date, responsibilities[] }` |
| `Project`          | `{ name, description, technologies[] }`              |
| `Certification`    | `{ name, issuer }`                                   |
| `Language`         | `{ name, proficiency }`                              |
| `CandidateProfile` | Full candidate model with skills, experience, education, preferred_roles, domains, strengths, weaknesses, embedding |
| `ResumeAnalysisResult` | Wrapper: `{ candidate_profile, embedding[], suggestions[], extracted_text }` |

### Job Domain Models (fastapi-ai)

| Model              | Description                                          |
|--------------------|------------------------------------------------------|
| `RawJob`           | Raw scraped job data: `{ title, company, location, description, apply_url, salary, employment_type, source }` |
| `JobProfile`       | Canonical AI job profile with skills, requirements, benefits, technologies, keywords, embedding |
| `JobAnalysisResult`| Wrapper: `{ job_profile, embedding[], normalized_job }` |

### Recommendation Models (fastapi-ai)

| Model                | Description                                        |
|----------------------|----------------------------------------------------|
| `RecommendationRequest`  | `{ candidate_profile_id: str }`                |
| `RecommendationItem`    | `{ title, company, location, description, employment_type, apply_url, similarity_score, recommendation_reason }` |
| `RecommendationResponse` | `{ recommendations: RecommendationItem[] }`    |
| `RecommendationResult`  | Internal: multi-score result with `semantic_score`, `skill_score`, `experience_score`, `location_score`, `education_score`, `final_score`, `matched_skills[]`, `missing_skills[]` |

### Database Tables (ai schema)

| Table                    | Description                                       |
|--------------------------|---------------------------------------------------|
| `ai.candidate_profiles`  | Stored candidate profiles with JSONB + pgvector    |
| `ai.job_profiles`        | Stored job profiles with JSONB + pgvector          |
| `ai.recommendation_results` | Multi-dimensional recommendation scores        |
| `ai.skill_gap`           | Skill match breakdown per recommendation          |
| `ai.ai_models`           | AI model and prompt version audit log             |
| `ai.processing_status`   | Async processing status tracker                   |
