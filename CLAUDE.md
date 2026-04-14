# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Run the application (starts on http://localhost:5001)
python app.py

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## Architecture

**Spendly** — A Flask-based personal expense tracking application (educational project).

**Stack:**
- Backend: Flask 3.1 with SQLite (via `database/db.py`)
- Frontend: Vanilla HTML/CSS/JS (no framework)
- Testing: pytest with pytest-flask

**Structure:**
```
expense-tracker/
├── app.py              # Flask app — all routes defined here
├── database/
│   └── db.py           # Database layer — students implement get_db(), init_db(), seed_db()
├── static/
│   ├── css/style.css   # All styles
│   └── js/main.js      # Client-side JavaScript (currently empty)
├── templates/
│   ├── base.html       # Base template with navbar/footer
│   ├── landing.html    # Homepage
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── terms.html      # Terms and conditions
│   └── privacy.html    # Privacy policy
└── requirements.txt
```

**Key patterns:**
- Jinja2 templates extend `base.html` which provides navbar, footer, and Google Fonts (DM Serif Display, DM Sans)
- CSS uses CSS variables for theming (ink/paper/accent palette)
- Routes in `app.py` are organized with comments marking implemented vs placeholder features
- Database module (`database/db.py`) is a student exercise — currently contains only stub comments

**Development context:**
This is a step-by-step educational project. Core files (`db.py`, `main.js`) are intentionally left incomplete for students to implement. When working here, check if a feature is meant to be built by the student before suggesting implementations.
