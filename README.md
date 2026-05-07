# Pinned

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Railway](https://img.shields.io/badge/deployed-Railway-blueviolet)

Pinned is a private social map app for friend groups. Instead of reading reviews from strangers on Google Maps or Yelp, you and your friends build a shared map together. Every pin is a real place someone in your circle has been to, and every review is from someone you actually trust.

Live at: https://pinned-production.up.railway.app

---

## How to Use the App

**Creating an Account**

Open the app and click Create Account. Enter a username, email, and password of at least 6 characters. Your account is stored in a real database so it persists across sessions.

**Dropping a Pin**

Tap anywhere on the map to open the pin form. Fill in the place name, choose a category such as Coffee, Bar, or Restaurant, select which group to share it with, write a short review, and give it a star rating. Hit Drop Pin and the pin appears on the map for everyone in that group.

**Groups**

Open the sidebar by clicking Menu and go to the Groups tab. Click Create New Group to make a new one, give it a name, choose an icon, and add friends by username. Each group has its own separate map layer and its own private chat. Click a group card to open that group's chat directly.

**Group Chat**

Click any group to open its private chat. Messages are completely isolated between groups. Click the group name in the chat header to see a dropdown of all members.

**Direct Messages**

Click the Chat button in the top right of the nav bar. This opens the Messages tab where every friend from your groups is listed individually. Click any name to open a 1-on-1 conversation. Each friend shows a pin count badge indicating how many places they have reviewed.

**Settings**

Click the Settings button in the nav to toggle Dark Mode, which switches the entire app and map to a dark colour scheme. You can also sign out from the settings panel.

---

## What Is Built

- Real user accounts with registration and login using JWT authentication
- Passwords are hashed with bcrypt and never stored in plain text
- Google Maps integration with a custom light blue style
- Drop pins anywhere on the map with a name, category, review, and star rating
- Private groups with member management and invite by username
- Per-group chat that is completely isolated between groups
- Direct messages for 1-on-1 conversations
- Pin count badges on friends in the DM list
- Personal pin counter in the nav bar
- Dark mode toggle that reskins the full app and map
- PostgreSQL database hosted on Railway for persistent storage
- Deployed live on Railway so anyone can use it

---

## What Is Still Being Built

- [ ] Live map sync so pins appear instantly for all group members without refreshing
- [x] Real-time chat using WebSockets instead of polling
- [ ] Invite friends via a shareable link rather than typing their username
- [ ] Photo uploads attached to pin reviews
- [ ] Push notifications when a friend drops a pin nearby
- [ ] User profile pages showing all pins and activity
- [ ] Search and filter pins by category, rating, or group member
- [ ] Mobile app built in React Native

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Vanilla JavaScript, HTML, CSS |
| Map | Google Maps JavaScript API |
| Auth | JWT tokens, bcrypt password hashing |
| Database | PostgreSQL hosted on Railway |
| Chat | HTTP polling |
| Deployment | Railway |

---

## Architecture

<img width="1101" height="815" alt="Arc" src="https://github.com/user-attachments/assets/bda2822d-b360-40d4-b950-fe584a272d8f" />

The app is split into a frontend served by the backend and a set of API endpoints that handle all data operations.

**Request flow**

When a user opens the app, their browser requests the page from the FastAPI backend which serves index.html via Jinja2 templating. The Google Maps JavaScript API is loaded directly by the browser using the API key injected into the HTML by the server. All subsequent interactions such as dropping pins, sending messages, and creating groups go through REST API calls to the backend with a JWT token in the Authorization header.

**Components**

The backend consists of four Python files. main.py contains all the API routes and the WebSocket connection manager. models.py defines the SQLAlchemy database models for users, groups, pins, reviews, and messages. database.py manages the connection to PostgreSQL using the DATABASE_URL environment variable. auth.py handles password hashing with bcrypt and JWT token creation and validation.

The frontend is a single HTML file served from the templates folder. It contains all the JavaScript, CSS, and HTML for the map, sidebar, chat, modals, and auth screens. It communicates with the backend via fetch calls and maintains the auth token in localStorage.

**Database**

PostgreSQL is hosted on Railway. The tables are created automatically on first startup via SQLAlchemy's create_all. The schema has seven tables: users, groups, group_members, pins, reviews, messages, and friendships.

**Authentication**

On registration, passwords are hashed with bcrypt before being stored. On login, the backend returns a

---

## Running Locally

The app requires the Python backend to be running. Do not open the HTML file directly or use VS Code Live Server as those will not work.

**Requirements:** Python 3.12 or higher

**Step 1. Clone the repository**

```bash
git clone https://github.com/alexho01/Pinned.git
cd Pinned
```

**Step 2. Create a virtual environment**

Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```

Mac and Linux:
```bash
python -m venv venv
source venv/bin/activate
```

**Step 3. Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4. Create a .env file**

Create a file called `.env` in the root of the project with the following:

```
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
DATABASE_URL=your_railway_postgres_internal_url_here
DATABASE_PUBLIC_URL=your_railway_postgres_public_url_here
SECRET_KEY=any_long_random_string_here
```

To get a Google Maps API key, go to console.cloud.google.com and enable the Maps JavaScript API.

To get the database URLs, create a free PostgreSQL database on railway.app and copy the connection strings from the Variables tab.

**Step 5. Start the server**

```bash
python -m uvicorn main:app --reload --port 8000
```

Open your browser and go to http://localhost:8000.

The server must stay running in the terminal for the app to work. If you close the terminal the app will stop responding. To keep it running, leave the terminal open or run it in a background process.

If you stop the server and want to start it again, open a new terminal in your Pinned folder and run:

```powershell
venv\Scripts\activate
python -m uvicorn main:app --reload --port 8000
```

You do not need to reinstall dependencies each time. Only the activate and uvicorn commands are needed on subsequent runs.

---

## Using the Live Version Instead

If you do not want to run it locally, the app is already deployed and running at:

https://pinned-production.up.railway.app

Anyone can create an account and use it from any device without setting anything up. The server on Railway runs 24 hours a day as long as the Railway project is active.

---

## Project Structure

```
Pinned/
|-- main.py          FastAPI backend, all API routes, auth, groups, pins, chat
|-- models.py        SQLAlchemy database models
|-- database.py      Database connection and session management
|-- auth.py          Password hashing and JWT token handling
|-- templates/
|   |-- index.html   Full frontend including map, sidebar, chat, and modals
|-- requirements.txt Python dependencies
|-- nixpacks.toml    Railway build configuration
|-- .env             Secret keys, not in version control
|-- .gitignore
|-- README.md
```

---

## Environment Variables

The .env file is never pushed to GitHub. Anyone cloning this repo needs to create their own .env with their own keys. The app will not start without a valid DATABASE_URL and GOOGLE_MAPS_API_KEY.

---

Built by [@alexho01](https://github.com/alexho01)
