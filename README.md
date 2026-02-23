# 🚀 CareerGuideAI — AI Career OS for Modern Talent

Personalized career intelligence, roadmap tracking, and professional reports—built like a production SaaS platform.

---

## 🌐 Live Demo
- **Web App**: https://career-guide-ai-2.onrender.com/

---

## 💡 Why CareerGuideAI
CareerGuideAI turns raw user inputs into structured, actionable career roadmaps with secure accounts, saved histories, and interactive checklist tracking.

---

## 🧠 Core Features
- **AI Career Guidance** with structured recommendations and match scores
- **Skill Gap Analysis** and targeted learning roadmaps
- **Interactive Checklist Roadmap** with progress tracking
- **Professional PDF Export** for shareable reports
- **Markdown Rendering** for clean, readable guidance output
- **User Authentication & Saved Roadmaps**
- **Redis Caching** for fast repeat responses
- **Async Task Processing** to prevent timeouts

---

## 🏗️ Architecture Overview
Modular, scalable Flask architecture with clean separation of concerns.

```
CareerGuideAI/
├── app.py                 # App factory + config
├── models.py              # SQLAlchemy models
├── routes/                # API + UI routes
│   ├── auth.py            # Register/login/logout
│   ├── api.py             # Core AI endpoints
│   ├── main.py            # UI routes
│   └── roadmaps.py        # Roadmap persistence
├── services/              # Business logic
│   ├── career_service.py  # AI guidance + caching
│   ├── roadmap_service.py # Checklist generation
│   └── report_service.py  # PDF generation
├── utils/                 # Shared helpers
│   ├── extensions.py      # db/cache/login/limiter
│   └── validation.py      # Pydantic validation
├── tasks.py               # Celery background tasks
├── templates/             # UI templates
├── static/                # Static assets
└── requirements.txt
```

---

## 🧰 Tech Stack
**Backend**
- Flask, SQLAlchemy, Flask-Login
- Pydantic validation
- Celery async jobs
- ReportLab PDF generation

**Frontend**
- Bootstrap 5, jQuery
- Marked.js + DOMPurify (safe markdown rendering)

**Infrastructure**
- PostgreSQL
- Redis (cache + Celery broker)
- Render (deployment)

---

## 🔐 Security & Production Readiness
- Secure password hashing (Werkzeug)
- Input validation via Pydantic
- Rate limiting per IP
- XSS-safe markdown rendering (DOMPurify)
- Environment-based secrets

---

## ⚡ Performance Optimizations
- Redis caching for repeated AI requests (1-hour TTL)
- Background AI tasks with Celery to avoid request timeouts
- Skeleton screens to improve perceived performance
- Reduced layout shifts on mobile

---

## 🗄️ Database & Caching
**PostgreSQL**
Stores users, roadmaps, and checklist progress.

**Redis**
Used for:
- Cached AI results
- Celery broker + result backend

---

## ✅ Interactive Roadmap Tracking
- AI output is converted into structured checklist items
- Users can mark items as complete
- Progress is stored in PostgreSQL per roadmap

---

## 🧪 Quick Start (Local)
```bash
git clone https://github.com/Amrut735/Career-Guide-AI.git
cd Career-Guide-AI
pip install -r requirements.txt
```

Create a `.env` file:
```
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/career_ai
REDIS_URL=redis://localhost:6379/0
```

Run the app:
```bash
python app.py
```

Run Celery worker:
```bash
celery -A tasks.celery worker -l info
```

---

## 🚀 Deployment (Render)
1. Connect GitHub repo to Render  
2. Build command: `pip install -r requirements.txt`  
3. Start command: `python app.py`  
4. Add env vars in Render dashboard  

---

## 🧪 Environment Variables
```
FLASK_SECRET_KEY=...
DATABASE_URL=...
REDIS_URL=...
```

---

## 🗺️ Product Roadmap
- ✅ Multi-roadmap persistence per user
- ✅ Async task processing
- ✅ PDF export
- 🔜 Analytics dashboard for user progress
- 🔜 Team/mentor sharing features
- 🔜 Role-based access control
- 🔜 Vector search for personalized recommendations

---

## 🤝 Contributing
We welcome contributions from the community.

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 📄 License
MIT License. See `LICENSE`.

---

Built with focus on career growth, product quality, and scalable engineering.
