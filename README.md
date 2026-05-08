# Pinned - Private Social Map App

> A full-stack social mapping platform that lets users create private maps with friends, drop location-based pins, write reviews, form groups, and message each other in real time.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Live App](#live-app)
- [Screenshots](#screenshots)
- [Core Features](#core-features)
- [Project Structure](#project-structure)
- [How the App Works](#how-the-app-works)
  - [Step 1 - User Authentication](#step-1---user-authentication)
  - [Step 2 - Friends and Groups](#step-2---friends-and-groups)
  - [Step 3 - Map Pins and Reviews](#step-3---map-pins-and-reviews)
  - [Step 4 - Messaging and Notifications](#step-4---messaging-and-notifications)
  - [Step 5 - Deployment](#step-5---deployment)
- [Database Design](#database-design)
- [API and Real-Time Features](#api-and-real-time-features)
- [Installation and Setup](#installation-and-setup)
- [Run Order](#run-order)
- [Technologies Used](#technologies-used)
- [Notes](#notes)
- [Future Improvements](#future-improvements)

---

## Project Overview

Pinned is a full-stack social mapping app built around a simple idea: place recommendations are more useful when they come from people you trust.

Instead of relying on public reviews from strangers, users can create private friend groups, drop pins on a shared Google Map, write reviews, and communicate through direct messages or group chat. Each group has its own map layer, so different friend groups can build separate collections of restaurants, cafes, study spots, parks, and other locations.

The core problem I wanted to solve was:

**"How can people save and share trusted place recommendations with their own friends instead of searching through anonymous reviews?"**

To build this, I developed a complete web application using FastAPI, PostgreSQL, SQLAlchemy, HTML, CSS, vanilla JavaScript, Google Maps JavaScript API, WebSockets, and Railway deployment. The app includes authentication, friend requests, blocking, private groups, map pins, reviews, real-time chat, unread notifications, and live map updates.

The public deployment has reached approximately **1,000+ users/downloads**.

---

## Live App

The project is deployed on Railway:

```text
https://pinned-production.up.railway.app
```

Anyone can create an account and use the app from a browser without installing anything locally.

---

## Screenshots

### Login and Account Creation

<img width="1902" height="917" alt="image" src="https://github.com/user-attachments/assets/e0ebf715-a8c5-4bbf-8ade-b57fe2b29b11" />

### Main Map Interface

Add a screenshot here showing the Google Map, pins, sidebar, and navigation.

```markdown
![Map Interface](images/map.png)
```

### Friends and Messages

Add a screenshot here showing the friend request panel, direct messages, or unread notifications.

```markdown
![Messages Interface](images/messages.png)
```

### Group Chat and Member Management

Add a screenshot here showing a group chat, group members dropdown, add friend to group option, and leave group button.

```markdown
![Group Chat](images/group-chat.png)
```

---

## Core Features

### User Accounts

- Users can register and log in with a username, email, and password
- Passwords are hashed with bcrypt before storage
- JWT tokens are used for authenticated requests
- User sessions persist through local storage
- Users can view profile information and personal pin count

### Interactive Map

- Google Maps JavaScript API integration
- Custom styled map interface
- Users can click anywhere on the map to drop a pin
- Each pin includes a place name, category, rating, and review
- Pins are connected to specific private groups
- Group members can see shared pins without needing to refresh the page
- Custom markers visually separate categories such as restaurants, cafes, parks, and other places

### Friends System

- Users can add friends by username
- The app prevents users from adding themselves
- The app prevents duplicate friend requests
- The app prevents adding users who are already friends
- Incoming friend requests appear as notifications
- Users can accept or decline requests
- Users can unfriend or block others through a three-dot menu
- Blocked users cannot continue sending friend requests

### Groups

- Users can create private groups with selected friends
- Groups have separate map layers and private chats
- Users can add new friends to an existing group without recreating it
- Users can click the group name to view group members
- Users can leave groups from the member dropdown
- Group member actions are protected through backend validation

### Messaging

- Private group chat for each group
- Direct messages between friends
- WebSocket-based real-time messaging
- Unread notification badges for direct messages and group messages
- Notifications stay visible until the user opens the specific chat
- Chat previews are shown in the messages list

---

## Project Structure

```text
Pinned/
│
├── main.py                 # FastAPI backend, API routes, WebSockets, groups, pins, chat, friends
├── models.py               # SQLAlchemy database models
├── database.py             # PostgreSQL connection and database session management
├── auth.py                 # Password hashing, JWT creation, and authentication checks
│
├── templates/
│   └── index.html          # Full frontend with map, sidebar, chat, modals, and client-side logic
│
├── requirements.txt        # Python dependencies
├── nixpacks.toml           # Railway build and deployment configuration
├── .gitignore              # Files ignored by Git
├── README.md               # Project documentation
└── .env                    # Local secrets and environment variables, not pushed to GitHub
```

> Note: The `.env` file should never be committed to GitHub. It stores private keys such as the database URL, Google Maps API key, and secret key.

---

## How the App Works

### Step 1 - User Authentication

**What it does:** Allows users to create an account, log in, and access protected app features.

When a user registers, the backend checks that the username and email are unique. The password is hashed using bcrypt before being saved to the database. When the user logs in, the backend verifies the password and returns a JWT token.

The frontend stores the token in local storage and attaches it to future API requests through the Authorization header.

Example authentication flow:

```text
User registers or logs in
Backend verifies credentials
Backend returns JWT token
Frontend stores token
Protected API requests include the token
Backend validates token before returning data
```

This allows routes such as pins, groups, friends, and messages to stay protected from unauthenticated users.

---

### Step 2 - Friends and Groups

**What it does:** Lets users connect with each other and organize private groups.

Users can search for friends by username and send a friend request. The backend prevents invalid requests, including sending a request to yourself, sending duplicate requests, or sending requests to someone who is already your friend.

Once a request is accepted, both users can message each other and add each other to private groups.

Groups are used to separate map activity. For example, a user could have one group for school friends, one group for family, and one group for travel planning. Each group has its own chat and map pins.

Group actions include:

- Create a group
- Add confirmed friends to a group
- Add new friends to an existing group
- View group members
- Leave a group
- Message group members
- Share pins with group members

---

### Step 3 - Map Pins and Reviews

**What it does:** Lets users save places to a shared Google Map.

When a user clicks on the map, the app opens a pin form. The user can enter a place name, select a category, choose a group, write a review, and add a star rating. The pin is saved to PostgreSQL and connected to the selected group.

Each pin stores:

| Field | Description |
|---|---|
| `lat` | Latitude of the pinned location |
| `lng` | Longitude of the pinned location |
| `name` | Name of the place |
| `type` | Category such as restaurant, coffee, park, or other |
| `group_id` | Group that can see the pin |
| `author_id` | User who created the pin |
| `created_at` | Time the pin was created |

Each review stores:

| Field | Description |
|---|---|
| `pin_id` | Pin connected to the review |
| `author_id` | User who wrote the review |
| `stars` | Rating value |
| `text` | Written review |
| `created_at` | Time the review was created |

Pins and reviews are shown on the map for group members. When a new pin is added, the app updates the map without requiring users to fully reload the page.

---

### Step 4 - Messaging and Notifications

**What it does:** Provides real-time direct messages, group chat, and notification badges.

Pinned uses WebSockets for real-time communication. This allows messages and notifications to appear quickly without requiring constant page refreshes.

Messaging features include:

- Direct messages between friends
- Group messages inside private groups
- Real-time updates through WebSockets
- Unread badges for direct messages
- Unread badges for group messages
- Friend request notifications
- Message notifications that remain until the relevant chat is opened

Example message flow:

```text
User sends a message
Backend saves message to PostgreSQL
Backend broadcasts the message through WebSocket
Recipient receives live update
Unread badge appears until the chat is opened
```

This makes the app feel closer to a real social platform rather than a static map project.

---

### Step 5 - Deployment

**What it does:** Runs the app publicly through Railway.

The app is deployed on Railway using a Python environment and a PostgreSQL database. Railway provides the public app URL, database hosting, environment variables, and deployment logs.

The `nixpacks.toml` file defines the build process. The backend runs with Uvicorn, and FastAPI serves both the API routes and the frontend page.

The live app is available at:

```text
https://pinned-production.up.railway.app
```

---

## Database Design

Pinned uses PostgreSQL with SQLAlchemy models. The main tables are:

| Table | Purpose |
|---|---|
| `users` | Stores account information and hashed passwords |
| `groups` | Stores private group information |
| `group_members` | Connects users to groups |
| `pins` | Stores map pin locations and metadata |
| `reviews` | Stores reviews and ratings for pins |
| `messages` | Stores group messages and direct messages |
| `friend_requests` | Stores pending friend requests |
| `friendships` | Stores accepted friend connections |
| `blocked_users` | Stores block relationships between users |

The database structure supports both social features and map-based features. Users can belong to many groups, groups can contain many users, and pins are connected to groups rather than being public to every user.

---

## API and Real-Time Features

The FastAPI backend handles the main app logic through protected API routes.

Important backend features include:

- User registration and login
- JWT validation
- Friend request creation and response
- Blocking and unfriending
- Group creation and member management
- Leaving groups
- Pin creation and review storage
- Group chat
- Direct messages
- WebSocket notifications

Real-time features are handled through WebSocket channels. These are used for:

- Group chat updates
- Direct message updates
- Friend request notifications
- Message notification badges
- Live map pin updates

---

## Installation and Setup

### What You Need

- Python 3.12 or higher
- PostgreSQL database
- Google Maps API key
- VS Code, PyCharm, or another code editor

### Clone the Project

```bash
git clone https://github.com/alexho01/Pinned.git
cd Pinned
```

### Create a Virtual Environment

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

### Install the Required Libraries

```bash
pip install -r requirements.txt
```

### Create the Environment File

Create a `.env` file in the root of the project:

```env
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
DATABASE_URL=your_database_url_here
DATABASE_PUBLIC_URL=your_database_public_url_here
SECRET_KEY=your_secret_key_here
```

To get a Google Maps API key, create a project in the Google Cloud Console and enable the Maps JavaScript API.

To get a PostgreSQL database URL, create a PostgreSQL database on Railway or another provider and copy the connection string.

---

## Run Order

After setup, start the backend server:

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

Then open the app in your browser:

```text
http://localhost:8000
```

Do not open `index.html` directly. The app needs the FastAPI backend running because authentication, database access, map keys, pins, groups, and messages all depend on backend routes.

If the server stops, open a terminal in the project folder and run the same commands again.

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

## Technologies Used

| Tool | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | API framework and backend server |
| SQLAlchemy | ORM for database models and queries |
| PostgreSQL | Persistent relational database |
| pg8000 | PostgreSQL driver |
| JWT | Token-based authentication |
| bcrypt | Password hashing |
| HTML | Frontend structure |
| CSS | Styling and responsive layout |
| JavaScript | Frontend interactivity |
| Google Maps JavaScript API | Interactive map and location pins |
| WebSockets | Real-time chat and notifications |
| Railway | Hosting, deployment, and PostgreSQL database |

---

## Notes

- The app must be run through the FastAPI server, not by opening the HTML file directly.
- The `.env` file should not be pushed to GitHub.
- The Google Maps API key should be restricted in Google Cloud for security.
- The Railway database stores user accounts, pins, reviews, messages, groups, and friend data.
- If database models change, existing deployed tables may need migration or a controlled reset.
- The live version can be used by anyone with the public Railway URL.

---

## Future Improvements

- Add photo uploads for pin reviews
- Add search and filtering by category, rating, group, or friend
- Add user profile pages with pin history and activity
- Add shareable invite links for friends and groups
- Add map clustering for large groups
- Add more detailed privacy controls for groups and pins
- Build a mobile version of the app

---

Built as a full-stack portfolio project to practise backend development, database design, real-time communication, API integration, and deployment.
