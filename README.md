# 🚀 Job Platform

A full-stack job platform application built with **Angular 17** and **Spring Boot 3.5**, designed to connect job seekers with opportunities. The platform features job browsing, intelligent recommendations, resume management, application tracking, and an admin dashboard.

---

## 📐 Architecture

This is a **monorepo** containing two independent submodules:

```
job-platform/
├── job-platform-api/    → Spring Boot REST API (Backend)
├── job-platform-ui/     → Angular 17 SPA (Frontend)
└── .gitmodules          → Git submodule configuration
```

| Layer      | Technology             | Repository |
|------------|------------------------|------------|
| **Frontend** | Angular 17, TypeScript, RxJS | [job-platform-ui](https://github.com/Raghavendra-Devale/job-platform-ui) |
| **Backend**  | Spring Boot 3.5, Java 17, JPA | [job-platform-api](https://github.com/Raghavendra-Devale/job-platform-api) |
| **Database** | PostgreSQL             | — |

---

## ✨ Features

### For Job Seekers
- 🔍 **Job Search & Browsing** — Filter and explore job listings
- 📄 **Resume Management** — Upload and manage multiple resumes
- 📋 **Application Tracking** — Track the status of all your applications
- 💾 **Saved Jobs** — Bookmark jobs to apply later
- 🤖 **Smart Recommendations** — Get personalized job suggestions based on your profile
- 👤 **Profile Management** — Build a comprehensive profile with skills, experience, and social links
- ⚙️ **Settings** — Manage account preferences and notifications

### For Admins
- 🛠️ **Admin Dashboard** — Manage platform content and users

### Platform
- 🔐 **JWT Authentication** — Secure login/registration with token-based auth
- 🔔 **Real-time Notifications** — Stay updated on application status changes
- 📊 **Dashboard Analytics** — Visual overview of job-seeking activity

---

## 🛠️ Prerequisites

| Tool        | Version   | Purpose              |
|-------------|-----------|----------------------|
| **Java**    | 17+       | Backend runtime      |
| **Maven**   | 3.8+      | Backend build tool   |
| **Node.js** | 18+       | Frontend runtime     |
| **npm**     | 9+        | Frontend dependencies|
| **PostgreSQL** | 14+    | Database             |

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone --recurse-submodules https://github.com/Raghavendra-Devale/job-platform.git
cd job-platform
```

> If you already cloned without submodules:
> ```bash
> git submodule update --init --recursive
> ```

### 2. Set Up the Database

```sql
CREATE DATABASE job_platform;
```

### 3. Start the Backend

```bash
cd job-platform-api
./mvnw spring-boot:run
```

The API will start on **http://localhost:8080**

### 4. Start the Frontend

```bash
cd job-platform-ui
npm install
npm start
```

The UI will start on **http://localhost:4200**

---

## 📖 Subproject Documentation

Each subproject has its own detailed README:

| Subproject | README |
|------------|--------|
| Backend API | [`job-platform-api/README.md`](./job-platform-api/README.md) |
| Frontend UI | [`job-platform-ui/README.md`](./job-platform-ui/README.md) |

---

## 🔗 API Documentation

Once the backend is running, Swagger UI is available at:

**http://localhost:8080/swagger-ui/index.html**

---

## 📂 Project Structure Overview

```
job-platform/
│
├── job-platform-api/                   # Spring Boot Backend
│   └── src/main/java/com/raghav/jobplatform/
│       ├── auth/                       # Authentication (login, register)
│       ├── jobs/                       # Job listings, applications, recommendations
│       ├── user/                       # User profiles & management
│       ├── config/                     # Security, JWT, REST client config
│       └── common/                     # Global exception handling
│
├── job-platform-ui/                    # Angular Frontend
│   └── src/app/
│       ├── core/                       # Services, models, guards, interceptors
│       ├── features/                   # Feature modules (jobs, auth, dashboard, etc.)
│       └── shared/                     # Navbar, toast, confirmation modal
│
├── .gitmodules                         # Submodule references
└── README.md                          # ← You are here
```

---

## 🧰 Tech Stack

### Backend
- **Spring Boot 3.5** — Application framework
- **Spring Data JPA** — Database ORM
- **Spring Security** — Authentication & authorization
- **Auth0 java-jwt** — JWT token generation/validation
- **jBCrypt** — Password hashing
- **Lombok** — Boilerplate reduction
- **SpringDoc OpenAPI** — Swagger API documentation
- **Spring Boot Actuator** — Health & monitoring endpoints
- **PostgreSQL** — Relational database

### Frontend
- **Angular 17** — Component framework with standalone components
- **TypeScript 5.4** — Type-safe JavaScript
- **RxJS 7.8** — Reactive programming
- **Angular Router** — Client-side routing with lazy loading & view transitions
- **Angular Animations** — UI transitions and micro-interactions

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is for learning and portfolio purposes.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Raghavendra-Devale">Raghavendra Devale</a>
</p>
