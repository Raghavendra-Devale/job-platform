# Local Development Setup Guide

This document provides step-by-step instructions for configuring and running the Job Platform locally on your workstation.

---

## 🛠️ Prerequisites & System Requirements

Ensure the following tools are installed before proceeding:

| Software Tool | Version | Purpose |
|---------------|---------|---------|
| **Java Development Kit (JDK)** | 17+ | Backend Spring Boot runtime |
| **Maven** | 3.8+ | Java project builder (wrapper script included) |
| **Python** | 3.12 | AI service engine runtime |
| **uv** | Latest | Faster Python package and virtual environment manager |
| **Node.js & npm** | Node 18+, npm 9+ | Frontend Angular build system |
| **PostgreSQL** | 16+ (with `pgvector`) | Relational database (also available in Docker Compose) |
| **Ollama** | Latest | Local host inference tool for LLMs |

---

## ⚡ Setup Instructions

### 1. Retrieve the Repository
Clone the monorepo including its Git submodules:
```bash
git clone --recurse-submodules https://github.com/Raghavendra-Devale/job-platform.git
cd job-platform
```
If you cloned the repository without submodules, initialize them:
```bash
git submodule update --init --recursive
```

### 2. Configure Ollama Local LLM
1. Download and start [Ollama](https://ollama.com).
2. Pull the required `llama3` completion model:
   ```bash
   ollama pull llama3
   ```
3. Keep the Ollama daemon running in the background (runs on port `11434` by default).

---

## 🚀 Option A: Running Locally (Recommended for Development)

Running each component natively allows hot-reloading and direct debugger attachments.

### Step 1: Start the PostgreSQL Database
Ensure your PostgreSQL instance is running. Connect via `psql` or PGAdmin and create the database:
```sql
CREATE DATABASE job_platform;
```
Ensure you have the `pgvector` extension installed. Run:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Step 2: Launch the FastAPI AI Service
1. Navigate to the AI folder:
   ```bash
   cd fastapi-ai
   ```
2. Copy the example environment template:
   ```bash
   cp .env.example .env
   ```
3. Configure `.env` values (the defaults are pre-configured for local execution):
   ```env
   PORT=8000
   AI_OLLAMA_BASE_URL=http://localhost:11434
   AI_EMBEDDING_MODEL=all-MiniLM-L6-v2
   AI_LLM_MODEL=llama3
   ```
4. Sync dependencies and run the server:
   ```bash
   uv sync
   uv run uvicorn app.main:app --reload --port 8000
   ```
The Swagger UI will be available at **http://localhost:8000/docs**

### Step 3: Run the Spring Boot Backend
1. Open a new terminal and navigate to the backend folder:
   ```bash
   cd job-platform-api
   ```
2. Set up environment variables. You can create a `.env` file or supply them directly to Spring. Default credentials:
   ```properties
   spring.datasource.url=jdbc:postgresql://localhost:5432/job_platform
   spring.datasource.username=postgres
   spring.datasource.password=postgres
   ```
3. Run the Spring Boot Maven task:
   ```bash
   # Windows PowerShell/Command Prompt
   ./mvnw.cmd spring-boot:run

   # Linux / macOS Shell
   ./mvnw spring-boot:run
   ```
The backend API will start on **http://localhost:8080** and Swagger UI on **http://localhost:8080/swagger-ui/index.html**

### Step 4: Run the Angular Frontend
1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd job-platform-ui
   ```
2. Install Angular UI package dependencies:
   ```bash
   npm install
   ```
3. Verify that `src/proxy.conf.json` points to the local backend gateway:
   ```json
   {
     "/api": {
       "target": "http://localhost:8080",
       "secure": false,
       "changeOrigin": true
     }
   }
   ```
4. Launch the Angular dev server:
   ```bash
   npm start
   ```
Navigate your browser to **http://localhost:4200** to interact with the UI.

---

## 🐳 Option B: Running with Docker Compose

To orchestrate and run all services in containers:

1. Validate the proxy configuration in `job-platform-ui/src/proxy.conf.json`. The target should be the container name:
   ```json
   {
     "/api": {
       "target": "http://job-platform-api:8080",
       "secure": false,
       "changeOrigin": true
     }
   }
   ```
2. Build and launch all services:
   ```bash
   docker compose up --build
   ```
3. The containers will expose:
   - **Angular UI:** http://localhost:4200
   - **Spring Boot API:** http://localhost:8080
   - **FastAPI AI:** http://localhost:8000
   - **PostgreSQL Database:** http://localhost:5432

---

## ⚙️ Configuration Reference

### Spring Boot Backend Properties (`application.properties`)
- `spring.datasource.url`: The PostgreSQL JDBC connection URL.
- `spring.jpa.hibernate.ddl-auto`: Set to `update` for automatic schema migrations.
- `ai.enabled`: Flag to enable or disable calling the FastAPI service.
- `ai.base-url`: Base endpoint URL of the FastAPI AI Engine (`http://localhost:8000`).

### FastAPI AI Engine Environment Variables (`.env`)
- `AI_PROVIDER`: The LLM engine provider (`ollama`).
- `AI_OLLAMA_BASE_URL`: API gateway to Ollama server.
- `AI_EMBEDDING_MODEL`: Hugging Face model identifier for vector generation (`all-MiniLM-L6-v2`).
- `AI_LLM_MODEL`: LLM name in Ollama for similarity match text summaries (`llama3`).
