# SmartHire 🚀
### AI-Powered Resume Analyzer, Job Tracker & Interview Prep Platform


> **SmartHire** is a full-stack AI-powered career platform that helps job seekers optimize their resumes, track job applications, generate interview questions, and polish their resume — all in one place.

---

## 🌐 Live Demo

| Service |             URL           |
|---------|---------------------------|
| 🎨 Frontend | https://smart-hire-pied-eta.vercel.app/|
| ⚙️ Backend API | https://smarthire-backend-vay0.onrender.com |
| 📖 API Docs |https://smarthire-backend-vay0.onrender.com/docs |

---

## ✨ Features

### 🤖 AI-Powered Resume Analysis
- **ATS Score** (0-100) with strict real-world scoring logic
- **Candidate Level Detection** (Fresher / Junior / Mid-Level / Senior)
- **Section Score Breakdown** (Keyword Match, Project Quality, Formatting, ATS Readability)
- **Missing Keywords Detection** with Critical / Important / Bonus classification
- **Quality Issues Detection** (missing links, no metrics, generic objective, etc.)
- **Resume Strengths** extraction from actual evidence
- **ATS Feedback** — keyword match and formatting analysis
- **Recruiter Feedback** — hiring simulation with RECOMMEND / MAYBE / REJECT decision

### ✍️ AI Resume Polisher
- Professional rewrite of resume content
- Strong action verbs and ATS-friendly language
- Side-by-side comparison (Original vs Polished)
- One-click copy of improved resume

### 🎤 AI Interview Question Generator
- **Technical Questions** — role and skill specific
- **HR Questions** — based on actual resume experience
- **Resume-Based Questions** — deep dive into candidate's projects
- Copy all questions with one click

### 📋 Job Application Tracker
- Full CRUD operations
- Status management (Saved → Applied → Interview → Offer → Rejected)
- Follow-up date tracking
- Notes for each application
- Job link storage

### 📊 ATS Score History
- Bar chart visualization of score progression
- Track improvement over multiple analyses
- Color-coded scores (Green / Yellow / Red)

### 🔐 Authentication & Security
- JWT-based secure authentication
- BCrypt password hashing
- Rate limiting on all sensitive endpoints
- Protected routes on frontend

---

## 🏗️ Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | REST API Framework |
| **Python 3.11** | Primary Language |
| **Google Gemini API** | AI Analysis Engine |
| **MongoDB Atlas** | Cloud Database |
| **Motor** | Async MongoDB Driver |
| **JWT (python-jose)** | Authentication |
| **pdfplumber** | PDF Text Extraction |
| **passlib[bcrypt]** | Password Hashing |
| **slowapi** | Rate Limiting |
| **pytest + httpx** | Automated Testing |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **React.js** | UI Framework |
| **Vite** | Build Tool |
| **Tailwind CSS** | Styling |
| **Axios** | HTTP Client |
| **React Router** | Client-side Routing |
| **Recharts** | Data Visualization |
| **Context API** | Global State Management |

### DevOps
| Technology | Purpose |
|-----------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container Orchestration |
| **Render** | Backend Deployment |
| **Vercel** | Frontend Deployment |
| **MongoDB Atlas** | Cloud Database Hosting |

---

## 📁 Project Structure

```
smarthire/
│
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py         # Register, Login
│   │   │   ├── resume.py       # Analyze, History, Rewrite, Interview Prep
│   │   │   └── jobs.py         # Job Tracker CRUD
│   │   ├── services/
│   │   │   ├── ai_services.py  # Gemini AI calls
│   │   │   ├── pdf_services.py # PDF text extraction
│   │   │   └── auth_services.py# JWT, Password hashing
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   └── job.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── resume.py
│   │   │   └── job.py
│   │   ├── middleware/
│   │   │   └── auth_middleware.py
│   │   └── database.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_resume.py
│   │   └── test_jobs.py
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── JobTracker.jsx
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ScoreCard.jsx
│   │   │   ├── SkillTags.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── api/
│   │   │   ├── auth.js
│   │   │   ├── resume.js
│   │   │   └── jobs.js
│   │   └── context/
│   │       └── AuthContext.jsx
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas Account
- Google Gemini API Key
- Docker (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/AnandBhagat345/smarthire.git
cd smarthire
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
```

Create `backend/.env`:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/smarthire
JWT_SECRET=your_super_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

```bash
# Run the server
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`
API Docs at: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
```

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

```bash
# Run the dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🐳 Docker Setup

Run the entire application with one command:

```bash
# Build and start all services
docker compose up --build

# Stop all services
docker compose down
```

Services will be available at:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

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
| Test File | Tests | Status |
|-----------|-------|--------|
| test_auth.py | 5 | ✅ Passed |
| test_jobs.py | 5 | ✅ Passed |
| test_resume.py | 4 | ✅ Passed |

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | Login & get JWT token | ❌ |

### Resume
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/resume/analyze` | AI resume analysis | ✅ |
| GET | `/resume/history` | Fetch analysis history | ✅ |
| POST | `/resume/rewrite` | AI resume polisher | ✅ |
| POST | `/resume/interview-prep` | Generate interview questions | ✅ |

### Jobs
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/jobs/` | Create job application | ✅ |
| GET | `/jobs/` | Get all applications | ✅ |
| PUT | `/jobs/{id}` | Update job status | ✅ |
| DELETE | `/jobs/{id}` | Delete application | ✅ |

---

## 🧠 AI Prompt Engineering

SmartHire uses carefully engineered prompts for each AI feature:

### Resume Analysis Prompt
- Strict ATS scoring with real hiring logic
- Candidate level detection (Fresher/Junior/Mid/Senior)
- Skill priority weighting (Critical/Important/Bonus)
- Quality issue detection
- Evidence-based strengths extraction
- Level-appropriate suggestions

### Resume Polisher Prompt
- Professional rewriting without fabricating experience
- Strong action verbs injection
- ATS-friendly language optimization
- JD keyword injection naturally

### Interview Question Generator Prompt
- Role-specific technical questions
- Resume-referenced HR questions
- Deep-dive project questions
- No generic questions — all specific to candidate

---

## 🔒 Security Features

- **JWT Authentication** — Stateless, 24-hour expiry
- **BCrypt Password Hashing** — One-way, salted
- **Rate Limiting** — Per IP address limits:
  - `/auth/register` → 5 req/min
  - `/auth/login` → 10 req/min
  - `/resume/analyze` → 5 req/min
  - `/resume/rewrite` → 5 req/min
  - `/resume/interview-prep` → 5 req/min
- **Protected Routes** — Frontend redirects unauthorized users
- **CORS Configuration** — Only authorized origins allowed

---

## 📊 ATS Scoring Logic

```
Total Score = 100 points

Keyword Match      = 50%
Project Quality    = 30%
Format & ATS       = 20%

Penalties:
- No GitHub links          → -5
- No measurable metrics    → -5
- Generic objective        → -5
- Missing critical skills  → -8 to -12 each
- Missing important skills → -4 to -6 each

Score Limits:
- Average Fresher    = 50-65
- Strong Fresher     = 65-75
- Exceptional        = max 80
- Near Perfect       = 85+
```

---

## 🌱 Environment Variables

### Backend (.env)
```env
MONGODB_URL=         # MongoDB Atlas connection string
JWT_SECRET=          # Secret key for JWT signing
GEMINI_API_KEY=      # Google Gemini API key
```

### Frontend (.env)
```env
VITE_API_URL=        # Backend API URL
```

---

## 🚀 Deployment

### Backend → Render
```
Runtime: Docker
Root Directory: backend/
Build: Docker build
Start: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend → Vercel
```
Framework: Vite
Root Directory: frontend/
Build Command: npm run build
Output Directory: dist
```

---

## 🔮 Future Enhancements

- [ ] Resume file storage (AWS S3)
- [ ] Resume version comparison
- [ ] LinkedIn job import
- [ ] Email reminders for follow-up dates
- [ ] Mobile application (React Native)
- [ ] Advanced job analytics dashboard
- [ ] CI/CD pipeline with GitHub Actions
- [ ] TypeScript migration
- [ ] WebSocket real-time notifications

---

## 👨‍💻 Author

**Anand Bhagat**
- GitHub: [@AnandBhagat345](https://github.com/AnandBhagat345)
- LinkedIn: [anand-raj345](https://www.linkedin.com/in/anand-raj345)
- Email: anandbhagat345@gmail.com

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/) for AI capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing Python framework
- [MongoDB Atlas](https://www.mongodb.com/atlas) for cloud database
- [Render](https://render.com/) for backend hosting
- [Vercel](https://vercel.com/) for frontend hosting

---

<div align="center">
  <strong>Built by Anand Bhagat</strong>
  <br/>
  <em>Final Year Project — B.Tech CSE (AI & ML) | GEC Aurangabad</em>
</div>