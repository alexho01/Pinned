# 📍 Pinned

A private social map app for friend groups. Drop location reviews as pins — only your crew sees them.

## Setup

```bash
# 1. Clone & enter
cd pinned

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
uvicorn main:app --reload --port 8000
```

Open **http://localhost:8000** in your browser.

## Features

- 🗺️ Real Google Maps with dark style
- 📍 Click anywhere on map to drop a pin + review
- 👥 Private groups with member list
- 💬 Real-time group chat (WebSocket)
- ⭐ Star ratings per review
- 🔴 Review count badges on pins

## Stack

- **Backend**: Python + FastAPI + WebSockets
- **Frontend**: Vanilla JS + Google Maps JS API
- **DB**: In-memory (swap for PostgreSQL + PostGIS for production)

## Next Steps

- Add PostgreSQL + PostGIS for persistent geo storage
- Add user auth (FastAPI Users or Auth0)
- Add photo uploads (S3)
- Deploy to Railway or Render
