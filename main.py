from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import datetime, uuid, os

app = FastAPI(title="Pinned")

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

templates = Jinja2Templates(directory="templates")

pins = [
    {"id": "1", "lat": 45.5088, "lng": -73.5541, "name": "Blue State Coffee",
     "type": "coffee", "group": "Weekend Crew",
     "reviews": [
         {"author": "Sophie L.", "initials": "SL", "stars": 5,
          "text": "Best oat latte in the city. Window seats are everything.", "time": "2h ago"},
         {"author": "Marcus K.", "initials": "MK", "stars": 4,
          "text": "Solid vibes, great WiFi. Gets busy around 10am.", "time": "Yesterday"},
     ]},
    {"id": "2", "lat": 45.5048, "lng": -73.5700, "name": "Le Boudoir",
     "type": "bar", "group": "Weekend Crew",
     "reviews": [
         {"author": "You", "initials": "ME", "stars": 5,
          "text": "Best cocktail menu around. Ask for the off-menu Midnight Garden.", "time": "1d ago"},
         {"author": "Jamie R.", "initials": "JR", "stars": 4,
          "text": "Perfect for a Friday night. Reservation recommended.", "time": "3d ago"},
     ]},
    {"id": "3", "lat": 45.5150, "lng": -73.5600, "name": "Pho Saigon 75",
     "type": "restaurant", "group": "Foodies MTL",
     "reviews": [
         {"author": "You", "initials": "ME", "stars": 5,
          "text": "24hr broth. Get the brisket pho with extra herbs. Cash only.", "time": "3d ago"},
     ]},
]

groups = [
    {"id": "g1", "name": "Weekend Crew",     "emoji": "🎉", "color": "#5aabf5",
     "members": ["Sophie L.", "Marcus K.", "Jamie R."]},
    {"id": "g2", "name": "Foodies MTL",      "emoji": "🍕", "color": "#f59e0b",
     "members": ["Sophie L.", "Alex B.", "Zoe K.", "Dan M.", "Priya S.", "Leo T."]},
    {"id": "g3", "name": "Date Night Spots", "emoji": "🌿", "color": "#a78bfa",
     "members": ["Sophie L."]},
]

chat_messages = {
    "g1": [
        {"author": "Sophie L.", "initials": "SL",
         "text": "Anyone tried that new ramen spot on St-Denis?", "time": "10:42 AM"},
        {"author": "Marcus K.", "initials": "MK",
         "text": "Not yet — should I drop a pin if I go this week?", "time": "10:45 AM"},
        {"author": "You", "initials": "ME",
         "text": "Yes! Pin everything!", "time": "10:47 AM"},
    ],
    "g2": [
        {"author": "Alex B.", "initials": "AB",
         "text": "Pho Saigon 75 is a must. Cash only FYI.", "time": "Yesterday"},
    ],
    "g3": [
        {"author": "Sophie L.", "initials": "SL",
         "text": "Le Boudoir Friday?", "time": "2d ago"},
    ],
}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "maps_api_key": GOOGLE_MAPS_API_KEY
    })

@app.get("/api/pins")
async def get_pins():
    return pins

@app.get("/api/groups")
async def get_groups():
    return groups

@app.post("/api/groups")
async def add_group(group: dict):
    groups.append(group)
    return group

@app.post("/api/pins")
async def add_pin(pin: dict):
    pin["id"] = str(uuid.uuid4())
    # Preserve reviews sent from frontend — do not wipe them
    if "reviews" not in pin:
        pin["reviews"] = []
    pins.append(pin)
    return pin

@app.get("/api/chat/{group_id}")
async def get_chat(group_id: str):
    return chat_messages.get(group_id, [])

@app.post("/api/chat/{group_id}")
async def post_message(group_id: str, msg: dict):
    if group_id not in chat_messages:
        chat_messages[group_id] = []
    msg["time"] = datetime.datetime.now().strftime("%I:%M %p")
    chat_messages[group_id].append(msg)
    return msg