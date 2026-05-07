# Pinned

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Railway](https://img.shields.io/badge/deployed-Railway-blueviolet)

Pinned is a private social map app for friend groups. Instead of relying on reviews from strangers, users can create shared maps with people they know. Friends can drop pins, write reviews, create groups, send messages, and build a trusted collection of places together.

Live app: https://pinned-production.up.railway.app

---

## Overview

Pinned combines a social messaging app with an interactive map. Users can create an account, add friends, form private groups, and save places to a shared Google Map. Each pin includes a place name, category, rating, and personal review. Groups have their own private chats and map layers, while direct messages allow friends to communicate individually.

The goal of Pinned is to make place recommendations more personal. Instead of searching through anonymous ratings, users can see where their friends have been and what they actually thought about those places.

---

## Features

### User Accounts and Authentication

- User registration and login
- JWT-based authentication
- Password hashing with bcrypt
- Persistent user sessions through local storage
- User profile modal with account information and personal pin count

### Interactive Map

- Google Maps JavaScript API integration
- Custom styled map interface
- Drop pins directly by clicking on the map
- Add a place name, category, star rating, and review
- Pins are connected to specific groups
- Group members can view shared pins on the map
- Pin and review updates appear without requiring a full page refresh

### Friends System

- Add friends by username
- Prevents users from adding themselves
- Prevents duplicate friend requests
- Prevents adding users who are already friends
- Friend requests appear as notifications
- Users can accept or decline incoming friend requests
- Users can unfriend or block others from the three-dot friend menu
- Blocked users cannot continue sending requests

### Groups

- Create private groups with selected friends
- Add confirmed friends when creating a group
- Add new friends to an existing group without remaking it
- View group members by clicking the group name
- Leave a group from the member dropdown
- Each group has its own private map layer and chat

### Messaging

- Group chat for each private group
- Direct messages between friends
- Real-time messaging using WebSockets
- Notification badges for unread group messages and direct messages
- Notifications remain visible until the user opens the relevant chat
- Chat previews and pin counts are shown in the messages list

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

Pinned uses a FastAPI backend that serves the frontend and handles all API requests. The frontend is built as a single HTML file with embedded CSS and JavaScript. It communicates with the backend through REST API calls and WebSocket connections.

### Request Flow

When a user opens the app, FastAPI serves `index.html` through Jinja2 templating. The backend injects the Google Maps API key into the page. After login, the frontend stores the JWT token and sends it in the Authorization header for protected requests.

User actions such as dropping pins, creating groups, sending messages, accepting friend requests, and blocking users are sent to the backend through API routes. Real-time actions such as messages, friend notifications, and pin updates are delivered through WebSockets.

### Backend Components

The backend is organized into several Python files:

- `main.py` contains the FastAPI routes, WebSocket logic, and main application behavior
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

The app uses PostgreSQL hosted on Railway. SQLAlchemy models are used to define and interact with the database tables.

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
