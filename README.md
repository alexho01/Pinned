# Pinned

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Railway](https://img.shields.io/badge/deployed-Railway-blueviolet)

Pinned is a full-stack social mapping platform that lets users create private maps with friends. Instead of relying on public reviews from strangers, users can save places, write reviews, form groups, and share recommendations with people they know.

Live app: https://pinned-production.up.railway.app

---

## Overview

Pinned combines an interactive map with social features such as friends, private groups, direct messages, group chat, and real-time notifications. Users can create accounts, add friends, create private groups, drop pins on a shared Google Map, write reviews, and communicate with others in real time.

Each pin is tied to a specific group, allowing different friend groups to maintain separate collections of places. This makes Pinned useful for organizing trusted recommendations for restaurants, cafes, study spots, parks, and other locations.

The project was built as a full-stack web application using FastAPI, PostgreSQL, SQLAlchemy, vanilla JavaScript, HTML, CSS, Google Maps JavaScript API, WebSockets, and Railway deployment.

---

## Key Features

### User Accounts and Authentication

- User registration and login
- JWT-based authentication
- Password hashing with bcrypt
- Protected API routes
- Persistent user sessions using local storage
- User profile modal with account details and personal pin count

### Interactive Map

- Google Maps JavaScript API integration
- Custom styled map interface
- Click-to-drop pin functionality
- Place name, category, rating, and review support
- Group-specific map layers
- Category-based custom markers
- Live pin and review updates without requiring a page refresh

### Friends System

- Add friends by username
- Prevents users from adding themselves
- Prevents duplicate friend requests
- Prevents adding users who are already friends
- Incoming friend request notifications
- Accept or decline friend requests
- Unfriend and block options through a three-dot menu
- Blocked users cannot send new requests or continue interaction

### Groups

- Create private groups with selected friends
- Add confirmed friends when creating a group
- Add new friends to an existing group without remaking it
- View all group members by clicking the group name
- Leave a group from the group member dropdown
- Each group has its own private chat and map layer

### Messaging and Notifications

- Real-time group chat
- Direct messages between friends
- WebSocket-based message delivery
- Unread message notification badges
- Notifications for group messages and direct messages
- Notifications remain visible until the user opens the relevant chat
- Chat previews and friend pin counts in the messages list

### Interface

- Responsive sidebar layout
- Groups and Messages tabs
- Profile button with pin count badge
- Settings panel
- Dark mode toggle
- Custom modals for pins, groups, friends, settings, and profile

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Map | Google Maps JavaScript API |
| Authentication | JWT, bcrypt |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Real-time Updates | WebSockets |
| Deployment | Railway |

---

## Architecture

<img width="1101" height="815" alt="Pinned architecture diagram" src="https://github.com/user-attachments/assets/bda2822d-b360-40d4-b950-fe584a272d8f" />

Pinned uses a FastAPI backend to serve the frontend and handle all API requests. The frontend is built as a single HTML file with embedded CSS and JavaScript. It communicates with the backend through REST API calls and WebSocket connections.

### Request Flow

When a user opens the app, FastAPI serves `index.html` through Jinja2 templating. The backend injects the Google Maps API key into the page. After login, the frontend stores the JWT token and sends it in the Authorization header for protected requests.

User actions such as creating groups, sending messages, accepting friend requests, blocking users, dropping pins, and writing reviews are sent to the backend through API routes. Real-time actions such as messages, friend notifications, and map updates are delivered through WebSockets.

### Backend Components

The backend is organized into several Python files:

- `main.py` contains FastAPI routes, WebSocket logic, and main application behavior
- `models.py` defines SQLAlchemy database models
- `database.py` manages the PostgreSQL database connection
- `auth.py` handles password hashing, JWT creation, and authentication checks

### Frontend Components

The frontend is located in `templates/index.html`. It includes:

- Authentication screen
- Google Map interface
- Sidebar navigation
- Group list and group chat
- Direct message list and DM chat
- Friend request interface
- Pin creation modal
- Profile and settings modals
- Client-side WebSocket handling

### Database

Pinned uses PostgreSQL hosted on Railway. SQLAlchemy models are used to define and interact with the database tables.

Main tables include:

- `users`
- `groups`
- `group_members`
- `pins`
- `reviews`
- `messages`
- `friend_requests`
- `friendships`
- `blocked_users`

---

## Running Locally

The app requires the FastAPI backend to be running. Do not open the HTML file directly and do not use VS Code Live Server. The frontend depends on backend API routes, authentication, database access, and server-rendered values.

### Requirements

- Python 3.12 or higher
- PostgreSQL database
- Google Maps API key

### Step 1. Clone the Repository

```bash
git clone https://github.com/alexho01/Pinned.git
cd Pinned
```

### Step 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
```

Mac and Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### Step 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4. Create a `.env` File

Create a file called `.env` in the root of the project:

```env
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
DATABASE_URL=your_database_url_here
DATABASE_PUBLIC_URL=your_database_public_url_here
SECRET_KEY=your_secret_key_here
```

To get a Google Maps API key, create a project in the Google Cloud Console and enable the Maps JavaScript API.

To get a PostgreSQL database URL, create a PostgreSQL database on Railway or another hosting provider and copy the connection string.

### Step 5. Start the Server

Windows PowerShell:

```powershell
venv\Scripts\activate
python -m uvicorn main:app --reload --port 8000
```

Mac and Linux:

```bash
source venv/bin/activate
python -m uvicorn main:app --reload --port 8000
```

Open the app in your browser:

```text
http://localhost:8000
```

Keep the terminal running while using the app. If the terminal is closed, the backend will stop and the app will no longer respond.

---

## Quick Start After Initial Setup

After you have already installed the dependencies and created your `.env` file, you only need to run:

Windows PowerShell:

```powershell
venv\Scripts\activate
python -m uvicorn main:app --reload --port 8000
```

Then open:

```text
http://localhost:8000
```

You do not need to reinstall dependencies every time.

---

## Optional Windows Shortcut

You can create a file called `run.bat` in the project folder:

```bat
@echo off
call venv\Scripts\activate
python -m uvicorn main:app --reload --port 8000
pause
```

After that, double-click `run.bat` to start the app locally.

---

## Using the Live Version

The app is deployed on Railway and can be accessed here:

https://pinned-production.up.railway.app

Users can create an account and use the app from any device without local setup.

---

## Project Structure

```text
Pinned/
|-- main.py             FastAPI backend, API routes, WebSockets, groups, pins, chat, friends
|-- models.py           SQLAlchemy database models
|-- database.py         Database connection and session management
|-- auth.py             Password hashing and JWT token handling
|-- templates/
|   |-- index.html      Frontend interface, map, chat, modals, and client-side logic
|-- requirements.txt    Python dependencies
|-- nixpacks.toml       Railway build configuration
|-- .env                Local environment variables, not committed to GitHub
|-- .gitignore
|-- README.md
```

---

## Environment Variables

The `.env` file is not committed to GitHub. Anyone cloning the repository must create their own `.env` file with valid credentials.

Required variables:

```env
GOOGLE_MAPS_API_KEY=
DATABASE_URL=
DATABASE_PUBLIC_URL=
SECRET_KEY=
```

The app will not work correctly without a valid database URL and Google Maps API key.

---

## Future Improvements

- Photo uploads for pin reviews
- Search and filter pins by category, rating, group, or friend
- User profile pages showing pin history and activity
- Shareable invite links for friends and groups
- Mobile app version
- Map clustering for larger groups
- More detailed privacy controls for groups and pins

---

## Author

Built by [@alexho01](https://github.com/alexho01)
