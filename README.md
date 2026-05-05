# Pinned

![Status](https://img.shields.io/badge/status-in%20development-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)

A private social map app for friend groups. You and your friends drop pins on a real Google Map for places you have been to, places you love, or places worth knowing about. Each pin holds reviews from everyone in your group, so instead of reading strangers on Yelp or Google Maps, you see what your actual friends thought.

---

## Important Note

This project is not finished. The app currently runs locally as a single user with placeholder friends. The biggest missing piece is real multi-user support, meaning right now you cannot actually invite your real friends and have them log in on their own devices. That is the next major thing being built. Everything you see in the current version works as a demonstration of what the app will do once accounts and live sync are added.

Do not open Index.HTML directly in a browser or through VS Code Live Server. The app will not work that way. It requires the Python backend to be running. See the setup section below.

---

## How It Works

When you run the app, the Python backend (FastAPI) starts a local server. Your browser connects to that server and loads the full interface. Everything you do, dropping pins, sending chat messages, creating groups, goes through the backend which stores it all in memory while the server is running.

The map is powered by the Google Maps JavaScript API. Pins are rendered as custom markers on top of a real map. Each pin shows a badge with how many reviews it has. Clicking a pin slides up a panel showing every review your group left for that place.

The sidebar has two tabs. The Groups tab shows all your groups and lets you click into each one, which slides open that group's private chat. The Messages tab shows all your friends as individual conversations, similar to direct messages on any other app. Each friend also shows a count of how many pins they have dropped, displayed like a streak counter.

Groups are completely separate from each other. A message sent in one group will never appear in another. Each group has its own pin layer on the map, its own chat history, and its own member list.

---

## What Is Built So Far

- Google Maps with a custom light blue style matching the app design
- Drop a pin anywhere on the map by clicking, with a name, type, review, and star rating
- Create groups and choose which friends are in each one
- Per-group chat where each group is fully isolated from the others
- Direct messages for 1-on-1 conversations with individual friends
- Add new friends through the Messages tab
- Pin count badges next to each friend in the DM list, showing how active they are
- A personal pin counter in the top nav showing how many pins you have dropped
- A member list dropdown inside each group chat
- Slide-in panels for group chats and DM conversations so you never leave the map view
- Click-away sidebar so the panel closes when you tap the map

---

## What Is Not Built Yet

The following features are planned and will be added as the project continues.

- [ ] User accounts with sign up and login
- [ ] Real friend invites via a link or username so actual people can join
- [ ] Persistent storage using PostgreSQL with PostGIS for geographic queries, so data does not disappear when the server restarts
- [ ] Live sync between multiple real users so everyone sees new pins appear in real time
- [ ] Photo uploads attached to reviews
- [ ] Push notifications when a friend drops a pin near your location
- [ ] A mobile app built in React Native
- [ ] Deployment to a public server so people can use it without running it locally

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Vanilla JavaScript, HTML, CSS |
| Map | Google Maps JavaScript API |
| Chat | HTTP polling per group |
| Storage | In-memory (PostgreSQL + PostGIS planned) |

---

## How to Run

Requirements: Python 3.10 or higher

```bash
# 1. Clone the repo
git clone https://github.com/alexho01/Pinned.git
cd Pinned

# 2. Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac and Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r Requirements.TXT

# 4. Start the server
python -m uvicorn Main:app --reload --port 8000
```

Then open http://localhost:8000 in your browser.

---

## Project Structure

```
Pinned/
|-- Main.py          FastAPI backend, all routes, chat API, pin and group storage
|-- Index.HTML       Full frontend, map, sidebar, chat, modals, all in one file
|-- Requirements.TXT Python dependencies
|-- README.md
```

---

## Contributing

This is a personal project in early development. Feel free to fork it or open issues. Once multi-user support is complete, proper contribution guidelines will be added.

Built by @alexho01
