# SmartHire 🚀

### AI-Powered Resume Analyzer, Job Tracker & Interview Prep Platform

> **SmartHire** is a full-stack AI-powered career platform that helps job seekers optimize their resumes, track job applications, generate interview questions, and polish their resume — all in one place.

---

## 🌐 Live Demo

| Service        | URL                                              |
| -------------- | ------------------------------------------------ |
| 🎨 Frontend    | https://smart-hire-pied-eta.vercel.app/          |
| ⚙️ Backend API | https://smarthire-backend-vay0.onrender.com      |
| 📖 API Docs    | https://smarthire-backend-vay0.onrender.com/docs |

---

## ✨ Features

### 🤖 AI-Powered Resume Analysis

* **ATS Score** (0-100) with strict real-world scoring logic
* **Candidate Level Detection** (Fresher / Junior / Mid-Level / Senior)
* **Section Score Breakdown** (Keyword Match, Project Quality, Formatting, ATS Readability)
* **Missing Keywords Detection** with Critical / Important / Bonus classification
* **Quality Issues Detection** (missing links, no metrics, generic objective, etc.)
* **Resume Strengths** extraction from actual evidence
* **ATS Feedback** — keyword match and formatting analysis
* **Recruiter Feedback** — hiring simulation with RECOMMEND / MAYBE / REJECT decision
* **Asynchronous AI Processing** using Celery + Redis for long-running resume analysis tasks
* **Real-time Task Status Updates** with frontend polling

### ✍️ AI Resume Polisher

* Professional rewrite of resume content
* Strong action verbs and ATS-friendly language
* Side-by-side comparison (Original vs Polished)
* One-click copy of improved resume

### 🎤 AI Interview Question Generator

* **Technical Questions** — role and skill specific
* **HR Questions** — based on actual resume experience
* **Resume-Based Questions** — deep dive into candidate's projects
* Copy all questions with one click

### 📋 Job Application Tracker

* Full CRUD operations
* Status management (Saved → Applied → Interview → Offer → Rejected)
* Follow-up date tracking
* Notes for each application
* Job link storage

### 📊 ATS Score History

* Bar chart visualization of score progression
* Track improvement over multiple analyses
* Color-coded scores (Green / Yellow / Red)

### 🔐 Authentication & Security

* JWT-based secure authentication
* BCrypt password hashing
* Rate limiting on all sensitive endpoints
* Protected routes on frontend

---

## 🏗️ Tech Stack

### Backend

| Technology            | Purpose                                 |
| --------------------- | --------------------------------------- |
| **FastAPI**           | REST API Framework                      |
| **Python 3.11**       | Primary Language                        |
| **Google Gemini API** | AI Analysis Engine                      |
| **MongoDB Atlas**     | Cloud Database                          |
| **Motor**             | Async MongoDB Driver                    |
| **Redis**             | Message Broker & Task Result Backend    |
| **Celery**            | Asynchronous Background Task Processing |
| **JWT (python-jose)** | Authentication                          |
| **pdfplumber**        | PDF Text Extraction                     |
| **passlib[bcrypt]**   | Password Hashing                        |
| **slowapi**           | Rate Limiting                           |
| **pytest + httpx**    | Automated Testing                       |

### Frontend

| Technology       | Purpose                 |
| ---------------- | ----------------------- |
| **React.js**     | UI Framework            |
| **Vite**         | Build Tool              |
| **Tailwind CSS** | Styling                 |
| **Axios**        | HTTP Client             |
| **React Router** | Client-side Routing     |
| **Recharts**     | Data Visualization      |
| **Context API**  | Global State Management |

### DevOps

| Technology         | Purpose                                |
| ------------------ | -------------------------------------- |
| **Docker**         | Containerization                       |
| **Docker Compose** | Multi-container Orchestration          |
| **Redis**          | Celery Message Broker & Result Backend |
| **Celery Worker**  | Background Task Processing             |
| **Render**         | Backend Deployment                     |
| **Vercel**         | Frontend Deployment                    |
| **MongoDB Atlas**  | Cloud Database Hosting                 |

---

## 📁 Project Structure

```text
smarthire/

│

├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py          # Register, Login
│   │   │   ├── resume.py        # Resume Analysis, History, Rewrite, Interview Prep
│   │   │   └── jobs.py          # Job Tracker CRUD
│   │   │
│   │   ├── services/
│   │   │   ├── ai_services.py   # Gemini AI calls
│   │   │   ├── pdf_services.py  # PDF text extraction
│   │   │   └── auth_services.py # JWT, Password hashing
│   │   │
│   │   ├── tasks/
│   │   │   └── resume_tasks.py  # Celery Background Resume Analysis Task
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   └── job.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── resume.py
│   │   │   └── job.py
│   │   │
│   │   ├── middleware/
│   │   │   └── auth_middleware.py
│   │   │
│   │   ├── celery_app.py        # Celery Configuration
│   │   └── database.py
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_resume.py
│   │   └── test_jobs.py
│   │
│   ├── .env.example             # Environment Variables Template
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── JobTracker.jsx
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ScoreCard.jsx
│   │   │   ├── SkillTags.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   │
│   │   ├── api/
│   │   │   ├── auth.js
│   │   │   ├── resume.js
│   │   │   └── jobs.js
│   │   │
│   │   └── context/
│   │       └── AuthContext.jsx
│   │
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml           # Multi-container Docker Configuration
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.11+
* Node.js 18+
* MongoDB Atlas Account
* Google Gemini API Key
* Redis
* Docker (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/AnandBhagat345/SmartHire.git

cd SmartHire
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate      # Windows

source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

Create `backend/.env`:

```env
MONGODB_URL=your_mongodb_url

SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_gemini_api_key
```

Start Redis locally before running Celery:

```bash
docker run -d -p 6379:6379 redis
```

Start the Celery worker:

```bash
celery -A app.celery_app.celery_app worker --loglevel=info
```

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

API Docs at: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

Run the dev server:

```bash
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🏗️ Async Resume Analysis Architecture

SmartHire uses an asynchronous background task architecture for AI-powered resume analysis.

Long-running operations such as PDF processing and Gemini AI analysis are handled outside the FastAPI request-response cycle.

```text
                    ┌─────────────────┐
                    │    Frontend     │
                    │   React + Vite  │
                    └────────┬────────┘
                             │
                             │ Submit Resume + JD
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │    Backend API  │
                    └────────┬────────┘
                             │
                             │ Create Background Task
                             ▼
                    ┌─────────────────┐
                    │      Redis      │
                    │ Message Broker  │
                    └────────┬────────┘
                             │
                             │ Task Queue
                             ▼
                    ┌─────────────────┐
                    │     Celery      │
                    │ Background Worker│
                    └────────┬────────┘
                             │
                             │ AI Analysis
                             ▼
                    ┌─────────────────┐
                    │  Google Gemini  │
                    │     AI API      │
                    └─────────────────┘

                             │
                             ▼

                    ┌─────────────────┐
                    │      Redis      │
                    │ Result Backend  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │ Task Status API │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Frontend     │
                    │ Status Polling  │
                    └─────────────────┘
```

### How Resume Analysis Works

1. User uploads a Resume and Job Description.
2. FastAPI receives and validates the request.
3. FastAPI creates a Celery background task and immediately returns a `task_id`.
4. Redis acts as the message broker and queues the task.
5. Celery Worker picks up the resume analysis task.
6. The worker extracts PDF content and sends the data to Google Gemini AI.
7. Celery stores the task result in Redis.
8. Frontend polls the `/task-status/{task_id}` endpoint.
9. Once the task is completed, the analysis result is displayed to the user.

This architecture prevents long-running AI operations from blocking the FastAPI server and improves application scalability.

---

## 🐳 Docker Setup

SmartHire can run as a complete multi-container application using Docker Compose.

### Docker Architecture

The application runs with four independent containers:

* **Frontend** → React + Vite
* **Backend** → FastAPI API Server
* **Celery Worker** → Background AI Task Processing
* **Redis** → Message Broker and Task Result Backend

```text
                    ┌─────────────────────┐
                    │      Frontend       │
                    │    React + Vite     │
                    │     Port 5173       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Backend       │
                    │       FastAPI       │
                    │     Port 8000       │
                    └──────────┬──────────┘
                               │
                   ┌───────────┴───────────┐
                   ▼                       ▼
        ┌──────────────────┐     ┌──────────────────┐
        │  Celery Worker   │◄───►│      Redis       │
        │ Background Tasks │     │ Broker + Results │
        └────────┬─────────┘     └──────────────────┘
                 │
                 ▼
        ┌──────────────────┐
        │   Google Gemini  │
        │      AI API      │
        └──────────────────┘
```

Run the entire application with one command:

```bash
# Build and start all services
docker compose up --build
```

Docker Compose automatically:

1. Builds the FastAPI backend container.
2. Builds the React frontend container.
3. Starts the Redis container.
4. Starts the Celery background worker.
5. Connects all services through the Docker network.

Stop all services:

```bash
docker compose down
```

Run in detached mode:

```bash
docker compose up -d --build
```

View all logs:

```bash
docker compose logs -f
```

View Celery worker logs:

```bash
docker compose logs -f celery_worker
```

Services will be available at:

* Frontend: `http://localhost:5173`
* Backend: `http://localhost:8000`
* API Docs: `http://localhost:8000/docs`

---

## 🧪 Running Tests

```bash
cd backend

venv\Scripts\activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

pytest tests/test_jobs.py -v
```

Current test status: **14/14 Passed ✅**

### Test Coverage

| Test File      | Tests | Status   |
| -------------- | ----- | -------- |
| test_auth.py   | 5     | ✅ Passed |
| test_jobs.py   | 5     | ✅ Passed |
| test_resume.py | 4     | ✅ Passed |

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint         | Description           | Auth |
| ------ | ---------------- | --------------------- | ---- |
| POST   | `/auth/register` | Register new user     | ❌    |
| POST   | `/auth/login`    | Login & get JWT token | ❌    |

### Resume

| Method | Endpoint                 | Description                    | Auth |
| ------ | ------------------------ | ------------------------------ | ---- |
| POST   | `/resume/analyze`        | Submit AI resume analysis task | ✅    |
| GET    | `/task-status/{task_id}` | Check background task status   | ✅    |
| GET    | `/resume/history`        | Fetch analysis history         | ✅    |
| POST   | `/resume/rewrite`        | AI resume polisher             | ✅    |
| POST   | `/resume/interview-prep` | Generate interview questions   | ✅    |

### Jobs

| Method | Endpoint     | Description            | Auth |
| ------ | ------------ | ---------------------- | ---- |
| POST   | `/jobs/`     | Create job application | ✅    |
| GET    | `/jobs/`     | Get all applications   | ✅    |
| PUT    | `/jobs/{id}` | Update job status      | ✅    |
| DELETE | `/jobs/{id}` | Delete application     | ✅    |

---

## 🧠 AI Prompt Engineering

SmartHire uses carefully engineered prompts for each AI feature:

### Resume Analysis Prompt

* Strict ATS scoring with real hiring logic
* Candidate level detection (Fresher/Junior/Mid/Senior)
* Skill priority weighting (Critical/Important/Bonus)
* Quality issue detection
* Evidence-based strengths extraction
* Level-appropriate suggestions

### Resume Polisher Prompt

* Professional rewriting without fabricating experience
* Strong action verbs injection
* ATS-friendly language optimization
* JD keyword injection naturally

### Interview Question Generator Prompt

* Role-specific technical questions
* Resume-referenced HR questions
* Deep-dive project questions
* No generic questions — all specific to candidate

---

## 🔒 Security Features

* **JWT Authentication** — Stateless, 24-hour expiry
* **BCrypt Password Hashing** — One-way, salted
* **Rate Limiting** — Per IP address limits:

  * `/auth/register` → 5 req/min
  * `/auth/login` → 10 req/min
  * `/resume/analyze` → 5 req/min
  * `/resume/rewrite` → 5 req/min
  * `/resume/interview-prep` → 5 req/min
* **Protected Routes** — Frontend redirects unauthorized users
* **CORS Configuration** — Only authorized origins allowed
* **Environment-based Secrets** — Sensitive credentials are excluded from version control

---

## 📊 ATS Scoring Logic

```text
Total Score = 100 points

Keyword Match      = 50%

Project Quality    = 30%

Format & ATS       = 20%

Penalties:

- No GitHub links          → -5

- No measurable metrics   → -5

- Generic objective       → -5

- Missing critical skills → -8 to -12 each

- Missing important skills → -4 to -6 each

Score Limits:

- Average Fresher    = 50-65

- Strong Fresher     = 65-75

- Exceptional        = max 80

- Near Perfect       = 85+
```

---

## 🌱 Environment Variables

SmartHire uses environment variables to securely manage sensitive configuration.

### Backend (`.env`)

Used for local development.

```env
MONGODB_URL=your_mongodb_url
SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

### Docker Environment (`.env.docker`)

Used by Docker containers for environment configuration.

This file may contain real credentials and should never be committed to GitHub.

### Environment Template (`.env.example`)

A safe template containing placeholder values.

```env
MONGODB_URL=your_mongodb_url
SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

Developers can copy the example file and add their own credentials.

```bash
cp .env.example .env
```

---

## 🚀 Deployment

### Backend → Render

```text
Runtime: Docker

Root Directory: backend/

Build: Docker build

Start: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend → Vercel

```text
Framework: Vite

Root Directory: frontend/

Build Command: npm run build

Output Directory: dist
```

---

## 🔮 Future Enhancements

* [ ] Resume file storage (AWS S3)
* [ ] Resume version comparison
* [ ] LinkedIn job import
* [ ] Email reminders for follow-up dates
* [ ] Mobile application (React Native)
* [ ] Advanced job analytics dashboard
* [ ] CI/CD pipeline with GitHub Actions
* [ ] TypeScript migration
* [ ] WebSocket real-time notifications

---

## 👨‍💻 Author

**Anand Bhagat**

* GitHub: [@AnandBhagat345](https://github.com/AnandBhagat345)
* LinkedIn: [anand-raj345](https://www.linkedin.com/in/anand-raj345)
* Email: [anandbhagat345@gmail.com](mailto:anandbhagat345@gmail.com)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

* [Google Gemini API](https://ai.google.dev/) for AI capabilities
* [FastAPI](https://fastapi.tiangolo.com/) for the amazing Python framework
* [MongoDB Atlas](https://www.mongodb.com/atlas) for cloud database
* [Redis](https://redis.io/) for message brokering and task result storage
* [Celery](https://docs.celeryq.dev/) for asynchronous task processing
* [Render](https://render.com/) for backend hosting
* [Vercel](https://vercel.com/) for frontend hosting

---

<div align="center">

<strong>Built by Anand Bhagat</strong>

<br/>

<em>Final Year Project — B.Tech CSE (AI & ML) | GEC Aurangabad</em>

</div>
