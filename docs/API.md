# Job Platform API Documentation

This document outlines the API endpoints exposed by both the **Spring Boot Backend (API Gateway)** and the **FastAPI AI Engine**.

---

## ☕ Spring Boot Backend (API Gateway)

All backend endpoints are relative to `http://localhost:8080` (or `http://job-platform-api:8080` inside Docker). Most endpoints require authentication via JWT token, either passed in an `Authorization: Bearer <token>` header or as an HttpOnly cookie named `jwt`.

### 🔑 Authentication

#### 1. Register User
- **Endpoint:** `POST /api/auth/register`
- **Authentication:** None (Public)
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "message": "User registered successfully"
  }
  ```
- **Response (400 Bad Request):**
  ```json
  {
    "error": "Email is already in use"
  }
  ```

#### 2. Login User
- **Endpoint:** `POST /api/auth/login`
- **Authentication:** None (Public)
- **Request Body:**
  ```json
  {
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }
  ```
- **Response (200 OK):**
  Sets an HttpOnly, Strict cookie named `jwt` containing the JWT token. Also returns the payload in the body:
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "USER"
  }
  ```

#### 3. Logout User
- **Endpoint:** `POST /api/auth/logout`
- **Authentication:** Required
- **Response (200 OK):**
  Clears the `jwt` HttpOnly cookie.
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

---

### 👤 User Profile & Preferences

#### 1. Get Profile & Preferences
- **Endpoint:** `GET /api/users/profile`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "USER",
    "activeResumeName": "resume_2026.pdf",
    "workPreference": "REMOTE",
    "alertEnabled": true,
    "createdAt": "2026-07-10T05:46:44",
    "experience": 5,
    "currentRole": "Software Engineer",
    "bio": "Experienced developer skilled in Java and Angular.",
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "portfolio": "https://johndoe.dev",
    "phone": "+1234567890",
    "location": "New York, USA",
    "preferredRoles": "Backend Engineer, Fullstack Developer",
    "preferredLocations": "Remote, New York",
    "remoteOnly": true,
    "salaryRange": "$100k - $130k",
    "jobTypes": "Full-time, Contract"
  }
  ```

#### 2. Update Profile Information
- **Endpoint:** `PUT /api/users/profile`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "experience": 6,
    "currentRole": "Senior Software Engineer",
    "bio": "Senior developer specializing in full stack architectures.",
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "portfolio": "https://johndoe.dev",
    "phone": "+1234567890",
    "location": "Boston, USA"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "message": "Profile updated successfully"
  }
  ```

#### 3. Change Password
- **Endpoint:** `POST /api/users/profile/change-password`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "currentPassword": "securepassword123",
    "newPassword": "newsecurepassword456"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "message": "Password changed successfully"
  }
  ```

#### 4. Update Profile Preferences
- **Endpoint:** `PUT /api/users/profile/preferences`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "workPreference": "REMOTE",
    "alertEnabled": true,
    "preferredRoles": "Senior Backend Engineer",
    "preferredLocations": "Remote",
    "remoteOnly": true,
    "salaryRange": "$120k - $150k",
    "jobTypes": "Full-time"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "message": "Preferences updated successfully"
  }
  ```

---

### 📄 Resume Management

#### 1. List Resumes
- **Endpoint:** `GET /api/users/profile/resumes`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "resumeName": "John_Doe_CV.pdf",
      "active": true,
      "updatedAt": "2026-07-10T06:12:30"
    }
  ]
  ```

#### 2. Upload Resume
- **Endpoint:** `POST /api/users/profile/resumes`
- **Authentication:** Required
- **Content Type:** `multipart/form-data`
- **Request Parameters:**
  - `file`: (Multipart file binary) Only PDF format is accepted, up to 10MB.
- **Response (210 Created):**
  Triggered asynchronously, parsing through the FastAPI AI service.
  ```json
  {
    "id": 1,
    "resumeName": "John_Doe_CV.pdf",
    "active": true,
    "updatedAt": "2026-07-10T06:12:30"
  }
  ```

#### 3. Activate Resume
- **Endpoint:** `PUT /api/users/profile/resumes/{id}/activate`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  {
    "message": "Resume activated successfully"
  }
  ```

#### 4. Rename Resume
- **Endpoint:** `PUT /api/users/profile/resumes/{id}/rename`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "resumeName": "John_Doe_Resume_2026.pdf"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "id": 1,
    "resumeName": "John_Doe_Resume_2026.pdf",
    "active": true,
    "updatedAt": "2026-07-10T06:15:00"
  }
  ```

#### 5. Delete Resume
- **Endpoint:** `DELETE /api/users/profile/resumes/{id}`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  {
    "message": "Resume deleted successfully"
  }
  ```

#### 6. Download Resume
- **Endpoint:** `GET /api/users/profile/resumes/{id}/download`
- **Authentication:** Required
- **Response (200 OK):**
  Returns the raw binary content of the PDF. Sets the header `Content-Disposition: attachment; filename="John_Doe_CV.pdf"` and `Content-Type: application/pdf`.

---

### 🔍 Jobs

#### 1. Paginated Job Listings
- **Endpoint:** `GET /api/jobs`
- **Authentication:** None (Public)
- **Query Parameters:**
  - `page`: (Integer, default 0) Page offset.
  - `size`: (Integer, default 10) Page size.
- **Response (200 OK):**
  ```json
  {
    "content": [
      {
        "id": 12,
        "title": "Software Engineer",
        "company": "TechCorp",
        "location": "Berlin, Germany",
        "source": "Arbeitnow",
        "remote": false,
        "tags": "Java, Spring Boot, SQL",
        "createdAt": "2026-07-09T18:22:00",
        "salary": "$80k - $95k",
        "jobType": "Full-time",
        "applyUrl": "https://arbeitnow.com/jobs/12"
      }
    ],
    "totalPages": 5,
    "totalElements": 48,
    "size": 10,
    "number": 0
  }
  ```

#### 2. Search Jobs with Filters
- **Endpoint:** `GET /api/jobs/search`
- **Authentication:** None (Public)
- **Query Parameters:**
  - `keyword`: (String, optional) Filters title/description.
  - `location`: (String, optional) Filters job locations.
  - `remoteOnly`: (Boolean, optional) Filter remote jobs.
  - `jobType`: (String, optional) e.g., "Full-time", "Part-time".
- **Response (200 OK):**
  ```json
  {
    "jobs": [
      {
        "id": 12,
        "title": "Software Engineer",
        "company": "TechCorp",
        "location": "Berlin, Germany",
        "source": "Arbeitnow",
        "remote": false,
        "tags": "Java, Spring Boot, SQL",
        "createdAt": "2026-07-09T18:22:00",
        "salary": "$80k - $95k",
        "jobType": "Full-time",
        "applyUrl": "https://arbeitnow.com/jobs/12"
      }
    ],
    "total": 1
  }
  ```

#### 3. Get Job Details
- **Endpoint:** `GET /api/jobs/{id}`
- **Authentication:** None (Public)
- **Response (200 OK):**
  If authenticated, access also records a recent view for the user.
  ```json
  {
    "id": 12,
    "externalJobId": "an-12345",
    "title": "Software Engineer",
    "company": "TechCorp",
    "location": "Berlin, Germany",
    "description": "<p>We are looking for a backend developer...</p>",
    "applyUrl": "https://arbeitnow.com/jobs/12",
    "salary": "$80k - $95k",
    "jobType": "Full-time",
    "source": "Arbeitnow",
    "remote": false,
    "tags": "Java, Spring Boot, SQL",
    "createdAt": "2026-07-09T18:22:00",
    "salaryMin": 80000,
    "salaryMax": 95000,
    "currency": "USD",
    "active": true
  }
  ```

#### 4. Trigger External Job Syncer
- **Endpoint:** `POST /api/jobs/sync`
- **Authentication:** Required (Admin level checking)
- **Response (200 OK):**
  ```json
  {
    "jobsProcessed": 100,
    "jobsImported": 34,
    "providerSummary": {
      "Arbeitnow": "34 jobs imported, 66 skipped",
      "RemoteOK": "0 jobs imported, 0 skipped"
    },
    "durationMs": 4250
  }
  ```

#### 5. Check External Provider Health
- **Endpoint:** `GET /api/providers/health`
- **Authentication:** None (Public)
- **Response (200 OK):**
  ```json
  {
    "Arbeitnow": "UP",
    "RemoteOK": "DOWN"
  }
  ```

#### 6. Dynamic Search External Jobs
- **Endpoint:** `GET /api/providers/search`
- **Authentication:** None (Public)
- **Query Parameters:**
  - `keyword`: (String, required) External search query.
- **Response (200 OK):**
  List of job details pulled live from external APIs without saving to local DB.

---

### 💾 Saved & Viewed Jobs

#### 1. Save a Job
- **Endpoint:** `POST /api/jobs/{jobId}/save`
- **Authentication:** Required
- **Response (201 Created):**
  ```json
  {
    "message": "Job saved successfully"
  }
  ```

#### 2. Unsave a Job
- **Endpoint:** `DELETE /api/jobs/{jobId}/save`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  {
    "message": "Job unsaved successfully"
  }
  ```

#### 3. Get Saved Jobs
- **Endpoint:** `GET /api/jobs/saved`
- **Authentication:** Required
- **Response (200 OK):**
  List of `JobListResponse` items.

#### 4. Get Saved Job IDs
- **Endpoint:** `GET /api/jobs/saved/ids`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  [12, 15, 23]
  ```

#### 5. Record Job View
- **Endpoint:** `POST /api/jobs/{jobId}/view`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  {
    "message": "Job view recorded"
  }
  ```

#### 6. Get Recently Viewed Jobs
- **Endpoint:** `GET /api/jobs/recent`
- **Authentication:** Required
- **Response (200 OK):**
  List of `JobListResponse` items viewed recently (limited to top 10).

---

### 🤖 Intelligent recommendations

#### 1. Generate Recommendations
- **Endpoint:** `POST /api/recommendations`
- **Authentication:** Required
- **Request Body (Optional `JobSearchCriteria`):**
  ```json
  {
    "preferredRoles": "Backend",
    "preferredLocations": "Remote",
    "remoteOnly": true,
    "salaryRange": "$100k+",
    "jobTypes": "Full-time"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "recommendations": [
      {
        "jobId": 12,
        "title": "Software Engineer",
        "company": "TechCorp",
        "score": 0.895,
        "matchReason": "Your experience with Java and Spring Boot matches the requirement for TechCorp's backend role."
      }
    ]
  }
  ```

---

### 📊 Dashboard & Applications Tracker

#### 1. Get Dashboard Summary
- **Endpoint:** `GET /api/dashboard/summary`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  {
    "activeResumeName": "John_Doe_CV.pdf",
    "totalResumes": 1,
    "savedJobs": 3,
    "applications": 2,
    "interviews": 1,
    "offers": 0,
    "recentActivities": [
      {
        "id": 45,
        "activityType": "APPLICATION_SUBMITTED",
        "description": "Applied to Software Engineer at TechCorp",
        "createdAt": "2026-07-10T08:00:00"
      }
    ]
  }
  ```

#### 2. Get Job Applications Tracker List
- **Endpoint:** `GET /api/dashboard/applications`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  [
    {
      "id": 5,
      "jobId": 12,
      "jobTitle": "Software Engineer",
      "company": "TechCorp",
      "location": "Berlin, Germany",
      "status": "APPLIED",
      "appliedAt": "2026-07-10T08:00:00",
      "updatedAt": "2026-07-10T08:00:00",
      "resumeName": "John_Doe_CV.pdf"
    }
  ]
  ```

#### 3. Submit a New Application Tracker
- **Endpoint:** `POST /api/dashboard/applications`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "jobId": 12
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 5,
    "jobId": 12,
    "jobTitle": "Software Engineer",
    "company": "TechCorp",
    "location": "Berlin, Germany",
    "status": "APPLIED",
    "appliedAt": "2026-07-10T08:00:00",
    "updatedAt": "2026-07-10T08:00:00",
    "resumeName": "John_Doe_CV.pdf"
  }
  ```

#### 4. Update Application Status
- **Endpoint:** `PUT /api/dashboard/applications/{id}/status`
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "status": "INTERVIEW"
  }
  ```
  *Valid Statuses:* `APPLIED`, `SCREENING`, `INTERVIEW`, `OFFER`, `REJECTED`.
- **Response (200 OK):**
  ```json
  {
    "message": "Application status updated successfully"
  }
  ```

#### 5. Delete Application Tracker
- **Endpoint:** `DELETE /api/dashboard/applications/{id}`
- **Authentication:** Required
- **Response (200 OK):**
  ```json
  {
    "message": "Application tracker deleted successfully"
  }
  ```

---

## ⚡ FastAPI AI Engine

All FastAPI endpoints are relative to `http://localhost:8000` (or `http://fastapi-ai:8000` inside Docker).

### 🩺 Health Diagnostic Check
- **Endpoint:** `GET /api/v1/health`
- **Response (200 OK):**
  ```json
  {
    "status": "UP",
    "embeddingProvider": "SentenceTransformerProvider",
    "llmProvider": "OllamaProvider",
    "version": "1.0.0"
  }
  ```

### 📄 Resume PDF Parser
- **Endpoint:** `POST /api/v1/resume/process`
- **Content Type:** `multipart/form-data`
- **Request Body:**
  - `file`: Uploaded resume PDF.
- **Response (200 OK):**
  ```json
  {
    "extracted_text": "Full text contents of PDF...",
    "summary": "AI summary of the candidate's experience.",
    "skills": [
      {
        "name": "Java",
        "rating": 5
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Science in Computer Science",
        "school": "Boston University",
        "dates": "2018 - 2022"
      }
    ],
    "experience": [
      {
        "role": "Software Developer",
        "company": "ByteScale",
        "dates": "2022 - Present",
        "responsibilities": "Developed scalable microservices..."
      }
    ],
    "certifications": ["AWS Certified Developer"],
    "projects": [
      {
        "name": "Job Platform App",
        "description": "Job portal with vector search matching",
        "tech_stack": "Angular, Spring Boot, Python"
      }
    ],
    "languages": ["English"]
  }
  ```

### 🤖 Generate Recommendation Matches
- **Endpoint:** `POST /api/v1/recommendations/generate`
- **Request Body:**
  ```json
  {
    "resume_text": "Experienced full stack engineer skilled in Java and Angular.",
    "jobs": [
      {
        "id": 12,
        "title": "Software Engineer",
        "company": "TechCorp",
        "description": "Looking for a backend developer with Java skills...",
        "location": "Berlin, Germany"
      }
    ]
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "recommendations": [
      {
        "jobId": 12,
        "title": "Software Engineer",
        "company": "TechCorp",
        "score": 0.895,
        "matchReason": "Your profile matches..."
      }
    ]
  }
  ```
