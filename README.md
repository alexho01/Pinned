# Pinned

![Status](https://img.shields.io/badge/status-in%20development-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)

Pinned is a private social map application for friend groups. Instead of reading reviews from strangers on Google Maps or Yelp, you and your friends build a shared map together. Every pin is a real place someone in your circle has been to, and every review is from someone you actually know.

The project is currently in active development. Core features including the map, groups, chat, and pin system are fully functional locally. The next major phase of development focuses on real user accounts, friend connections, and live multi-user sync so that different people can use the app from their own devices.

---

## Features

**Map and Pins**

Click the Drop Pin button in the top right, tap any location on the map, and fill in the details. Each pin includes a place name, category, star rating, and a written review. Pins are grouped by your friend groups and show a badge indicating how many reviews they have received. Clicking a pin opens a review panel showing every review that group has left for that place.

**Groups**

Open the sidebar and go to the Groups tab. Click Create New Group to set up a group, give it a name, choose an icon, and select which friends to add. You can have multiple groups for different social circles such as school friends, family, or coworkers. Each group has its own separate pin layer on the map and its own private chat.

**Group Chat**

Click on any group from the Groups tab to open that group's chat. Messages are completely isolated between groups. A message sent in one group will never appear in another. The chat header shows the group name and clicking it reveals a dropdown list of all members.

**Direct Messages**

Switch to the Messages tab to see all your friends listed individually. Click any friend to open a 1-on-1 conversation. Each friend displays a pin count badge showing how many places they have reviewed, similar to a streak counter. Use the add friend button in the top right of the Messages tab to add new friends.

**Pin Counts**

Your personal pin count is displayed in the top right of the navigation bar next to the Drop Pin button. This updates every time you drop a new pin.

---

## Current Status

This version runs locally as a single user. The placeholder friends and sample data exist to demonstrate what the finished product will look like. Real accounts and live connections between multiple users are the next major milestone.

Do not open the HTML file directly in a browser or through a static file server such as VS Code Live Server. The application requires the Python backend to be running. All map interactions, chat messages, pin drops, and group management go through the FastAPI server.

---

## Roadmap

The following features are planned for upcoming development phases.

**Multi-User Support**
- [ ] User accounts with registration and login
- [ ] Secure authentication using JWT tokens or OAuth
- [ ] Friend system with invite links and username search
- [ ] Profile pages showing a user's pinned places and activity

**Real-Time Sync**
- [ ] Live map updates so all group members see new pins instantly
- [ ] Real-time chat using WebSockets
- [ ] Online presence indicators showing which friends are active

**Data and Storage**
- [ ] Persistent database using PostgreSQL with PostGIS for geographic queries
- [ ] Data does not disappear when the server restarts
- [ ] Pin history and user activity tracking

**Additional Features**
- [ ] Photo uploads attached to reviews
- [ ] Push notifications when a friend drops a pin nearby
- [ ] Search and filter pins by category, rating, or group member
- [ ] Mobile application built in React Native

**Deployment**
- [ ] Host on a public server so users do not need to run it locally
- [ ] Environment-based configuration for production vs development

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Vanilla JavaScript, HTML, CSS |
| Map | Google Maps JavaScript API |
| Chat | HTTP polling, WebSockets planned |
| Storage | In-memory, PostgreSQL with PostGIS planned |

---

## Setup

**Requirements:** Python 3.10 or higher

**Step 1. Clone the repository**

```bash
git clone https://github.com/alexho01/Pinned.git
cd Pinned
```

**Step 2. Create a virtual environment**

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Mac and Linux:
```bash
source venv/bin/activate
```

**Step 3. Install dependencies**

```bash
pip install -r Requirements.txt
```

**Step 4. Set up your Google Maps API key**

Create a file called `.env` in the root of the project and add the following line:

```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

You can obtain a free API key from console.cloud.google.com. Make sure to enable the Maps JavaScript API in your Google Cloud project. The `.env` file is excluded from version control and will never be pushed to GitHub.

**Step 5. Start the server**

```bash
python -m uvicorn main:app --reload --port 8000
```

Open your browser and go to http://localhost:8000.

---

## Project Structure

```
Pinned/
|-- main.py              FastAPI backend, API routes, chat, pin and group storage
|-- templates/
|   |-- index.html       Full frontend including map, sidebar, chat, and modals
|-- .env                 API keys, not included in version control
|-- .gitignore
|-- Requirements.txt     Python dependencies
|-- README.md
```

---

## Contributing

This is a personal project in early development. Feel free to fork the repository or open issues with suggestions. Contribution guidelines will be added once the multi-user foundation is in place.

---

Built by [@alexho01](https://github.com/alexho01)
