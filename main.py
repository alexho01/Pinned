from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, or_, func
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from database import get_db, engine
from models import Base, User, Group, Pin, Review, Message, group_members
from auth import hash_password, verify_password, create_token, get_current_user
import datetime, os, json, uuid

load_dotenv()


# ── Friend system tables ──
# These live here so you do not need to edit models.py. Base.metadata.create_all()
# will create the tables on startup if they do not already exist.
class Friendship(Base):
    __tablename__ = "friendships"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_a_id = Column(String, ForeignKey("users.id"), nullable=False)
    user_b_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint("user_a_id", "user_b_id", name="uq_friendship_pair"),)

class FriendRequest(Base):
    __tablename__ = "friend_requests"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    from_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint("from_user_id", "to_user_id", name="uq_friend_request_pair"),)

class BlockedUser(Base):
    __tablename__ = "blocked_users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    blocker_id = Column(String, ForeignKey("users.id"), nullable=False)
    blocked_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint("blocker_id", "blocked_id", name="uq_blocked_pair"),)

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pinned")
templates = Jinja2Templates(directory="templates")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

# ── WebSocket connection manager ──
class ConnectionManager:
    def __init__(self):
        # group_id -> list of (websocket, user_id)
        self.connections: dict[str, list[tuple]] = {}

    async def connect(self, ws: WebSocket, group_id: str, user_id: str):
        await ws.accept()
        if group_id not in self.connections:
            self.connections[group_id] = []
        self.connections[group_id].append((ws, user_id))

    def disconnect(self, ws: WebSocket, group_id: str):
        if group_id in self.connections:
            self.connections[group_id] = [
                (w, u) for w, u in self.connections[group_id] if w != ws
            ]

    async def broadcast(self, group_id: str, data: dict):
        if group_id not in self.connections:
            return
        dead = []
        for ws, uid in self.connections[group_id]:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.append((ws, uid))
        for item in dead:
            self.connections[group_id].remove(item)

manager = ConnectionManager()

# ── Pydantic schemas ──
class RegisterBody(BaseModel):
    username: str
    email: str
    password: str

class LoginBody(BaseModel):
    username: str
    password: str

class GroupBody(BaseModel):
    name: str
    emoji: Optional[str] = "👥"
    color: Optional[str] = "#5aabf5"

class PinBody(BaseModel):
    lat: float
    lng: float
    name: str
    type: Optional[str] = "other"
    group_id: str
    stars: Optional[int] = 5
    review_text: Optional[str] = ""

class MessageBody(BaseModel):
    text: str

class InviteBody(BaseModel):
    username: str

class FriendBody(BaseModel):
    username: str

# ── Pages ──
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "maps_api_key": GOOGLE_MAPS_API_KEY
    })

# ── Auth ──
@app.post("/api/auth/register")
def register(body: RegisterBody, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(400, "Username already taken")
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already registered")
    if len(body.password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    user = User(username=body.username, email=body.email,
                password_hash=hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.id)
    return {"token": token, "user": {"id": user.id, "username": user.username}}

@app.post("/api/auth/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Incorrect username or password")
    token = create_token(user.id)
    return {"token": token, "user": {"id": user.id, "username": user.username}}

@app.get("/api/auth/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}

# ── Groups ──
@app.get("/api/groups")
def get_groups(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return [
        {"id": g.id, "name": g.name, "emoji": g.emoji, "color": g.color,
         "members": [{"id": m.id, "username": m.username} for m in g.members]}
        for g in current_user.groups
    ]

@app.post("/api/groups")
def create_group(body: GroupBody, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = Group(name=body.name, emoji=body.emoji, color=body.color, owner_id=current_user.id)
    group.members.append(current_user)
    db.add(group)
    db.commit()
    db.refresh(group)
    return {"id": group.id, "name": group.name, "emoji": group.emoji, "color": group.color,
            "members": [{"id": m.id, "username": m.username} for m in group.members]}

@app.post("/api/groups/{group_id}/invite")
def invite_to_group(group_id: str, body: InviteBody,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(404, "Group not found")
    if current_user not in group.members:
        raise HTTPException(403, "You are not in this group")
    invitee = db.query(User).filter(User.username == body.username).first()
    if not invitee:
        raise HTTPException(404, f"User '{body.username}' not found")
    if invitee in group.members:
        raise HTTPException(400, "User is already in this group")
    group.members.append(invitee)
    db.commit()
    return {"ok": True, "username": invitee.username}

# ── Pins ──
@app.get("/api/pins")
def get_pins(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group_ids = [g.id for g in current_user.groups]
    pins = db.query(Pin).filter(Pin.group_id.in_(group_ids)).all()
    return [_pin_dict(p) for p in pins]

@app.post("/api/pins")
async def create_pin(body: PinBody, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == body.group_id).first()
    if not group or current_user not in group.members:
        raise HTTPException(403, "Not a member of this group")
    pin = Pin(lat=body.lat, lng=body.lng, name=body.name, type=body.type,
              group_id=body.group_id, author_id=current_user.id)
    db.add(pin)
    db.flush()
    review = Review(pin_id=pin.id, author_id=current_user.id,
                    stars=body.stars, text=body.review_text)
    db.add(review)
    db.commit()
    db.refresh(pin)
    data = _pin_dict(pin)
    # Broadcast new pin to all group members via WebSocket
    await manager.broadcast(body.group_id, {"type": "new_pin", "pin": data})
    return data

# ── Chat ──
@app.get("/api/chat/{group_id}")
def get_messages(group_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group or current_user not in group.members:
        raise HTTPException(403, "Not a member of this group")
    msgs = db.query(Message).filter(Message.group_id == group_id).order_by(Message.created_at).all()
    return [_msg_dict(m) for m in msgs]

@app.post("/api/chat/{group_id}")
async def post_message(group_id: str, body: MessageBody,
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group or current_user not in group.members:
        raise HTTPException(403, "Not a member of this group")
    msg = Message(group_id=group_id, author_id=current_user.id, text=body.text)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    data = _msg_dict(msg)
    await manager.broadcast(group_id, {"type": "new_message", "message": data})
    return data

# ── DMs ──
@app.get("/api/dm/{friend_id}")
def get_dm(friend_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not _is_friend(db, current_user.id, friend_id) or _is_blocked(db, current_user.id, friend_id):
        raise HTTPException(403, "You can only message friends")
    msgs = db.query(Message).filter(
        Message.dm_to_id != None,
        ((Message.author_id == current_user.id) & (Message.dm_to_id == friend_id)) |
        ((Message.author_id == friend_id) & (Message.dm_to_id == current_user.id))
    ).order_by(Message.created_at).all()
    return [_msg_dict(m) for m in msgs]

@app.post("/api/dm/{friend_id}")
async def post_dm(friend_id: str, body: MessageBody,
                  current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    if not _is_friend(db, current_user.id, friend_id) or _is_blocked(db, current_user.id, friend_id):
        raise HTTPException(403, "You can only message friends")
    msg = Message(dm_to_id=friend_id, author_id=current_user.id, text=body.text)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    data = _msg_dict(msg)
    a, b = _friend_pair(current_user.id, friend_id)
    dm_channel = f"dm_{a}_{b}"
    await manager.broadcast(dm_channel, {"type": "new_dm", "message": data})
    return data

# ── Friends ──
def _norm_username(name: str) -> str:
    return (name or "").strip().lower()

def _friend_pair(a: str, b: str) -> tuple[str, str]:
    a, b = str(a), str(b)
    return (a, b) if a < b else (b, a)

def _get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(func.lower(User.username) == _norm_username(username)).first()

def _is_friend(db: Session, user_a_id: str, user_b_id: str) -> bool:
    a, b = _friend_pair(user_a_id, user_b_id)
    return db.query(Friendship).filter(
        Friendship.user_a_id == a,
        Friendship.user_b_id == b
    ).first() is not None

def _is_blocked(db: Session, user_a_id: str, user_b_id: str) -> bool:
    return db.query(BlockedUser).filter(
        or_(
            (BlockedUser.blocker_id == str(user_a_id)) & (BlockedUser.blocked_id == str(user_b_id)),
            (BlockedUser.blocker_id == str(user_b_id)) & (BlockedUser.blocked_id == str(user_a_id))
        )
    ).first() is not None

def _make_friendship(db: Session, user_a_id: str, user_b_id: str) -> None:
    a, b = _friend_pair(user_a_id, user_b_id)
    if not db.query(Friendship).filter(Friendship.user_a_id == a, Friendship.user_b_id == b).first():
        db.add(Friendship(user_a_id=a, user_b_id=b))

def _friend_request_dict(req: FriendRequest, db: Session) -> dict:
    sender = db.query(User).filter(User.id == req.from_user_id).first()
    return {
        "id": req.id,
        "from_id": req.from_user_id,
        "from_username": sender.username if sender else "Unknown",
        "time": req.created_at.strftime("%b %d")
    }

@app.get("/api/friends")
def get_friends(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Friendship).filter(
        or_(Friendship.user_a_id == current_user.id, Friendship.user_b_id == current_user.id)
    ).all()
    friend_ids = [r.user_b_id if r.user_a_id == current_user.id else r.user_a_id for r in rows]
    if not friend_ids:
        return []
    users = db.query(User).filter(User.id.in_(friend_ids)).all()
    friends = []
    for u in users:
        if _is_blocked(db, current_user.id, u.id):
            continue
        pin_count = db.query(Review).filter(Review.author_id == u.id).count()
        friends.append({"id": u.id, "username": u.username, "pin_count": pin_count})
    friends.sort(key=lambda f: f["username"].lower())
    return friends

@app.post("/api/friends/request")
async def send_friend_request(body: FriendBody,
                              current_user: User = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    username = body.username.strip()
    if not username:
        raise HTTPException(400, "Enter a username")
    if _norm_username(username) == _norm_username(current_user.username):
        raise HTTPException(400, "You cannot add yourself")

    target = _get_user_by_username(db, username)
    if not target:
        raise HTTPException(404, "User not found")
    if _is_blocked(db, current_user.id, target.id):
        raise HTTPException(403, "You cannot send a request to this user")
    if _is_friend(db, current_user.id, target.id):
        raise HTTPException(400, "This user is already your friend")

    # If they already requested you, tell the user to accept that request instead.
    incoming = db.query(FriendRequest).filter(
        FriendRequest.from_user_id == target.id,
        FriendRequest.to_user_id == current_user.id
    ).first()
    if incoming:
        raise HTTPException(400, "This user already sent you a request. Open Requests to accept it.")

    existing = db.query(FriendRequest).filter(
        FriendRequest.from_user_id == current_user.id,
        FriendRequest.to_user_id == target.id
    ).first()
    if existing:
        raise HTTPException(400, "Friend request already sent")

    req = FriendRequest(from_user_id=current_user.id, to_user_id=target.id)
    db.add(req)
    db.commit()
    db.refresh(req)
    data = _friend_request_dict(req, db)
    await manager.broadcast(f"notif_{target.id}", {"type": "friend_request", "request": data})
    return {"ok": True, "request": data}

@app.get("/api/friends/requests")
def get_friend_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    requests = db.query(FriendRequest).filter(FriendRequest.to_user_id == current_user.id).all()
    return [_friend_request_dict(r, db) for r in requests if not _is_blocked(db, current_user.id, r.from_user_id)]

@app.post("/api/friends/request/{request_id}/accept")
async def accept_friend_request(request_id: str,
                                current_user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    req = db.query(FriendRequest).filter(
        FriendRequest.id == request_id,
        FriendRequest.to_user_id == current_user.id
    ).first()
    if not req:
        raise HTTPException(404, "Friend request not found")
    if _is_blocked(db, current_user.id, req.from_user_id):
        raise HTTPException(403, "This user is blocked")

    _make_friendship(db, current_user.id, req.from_user_id)
    sender = db.query(User).filter(User.id == req.from_user_id).first()
    db.delete(req)
    db.commit()
    await manager.broadcast(f"notif_{req.from_user_id}", {
        "type": "friend_accepted",
        "username": current_user.username,
        "friend": {"id": current_user.id, "username": current_user.username, "pin_count": 0}
    })
    return {"ok": True, "friend": {"id": sender.id, "username": sender.username} if sender else None}

@app.post("/api/friends/request/{request_id}/decline")
def decline_friend_request(request_id: str,
                           current_user: User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    req = db.query(FriendRequest).filter(
        FriendRequest.id == request_id,
        FriendRequest.to_user_id == current_user.id
    ).first()
    if not req:
        raise HTTPException(404, "Friend request not found")
    db.delete(req)
    db.commit()
    return {"ok": True}

@app.delete("/api/friends/{username}")
def unfriend(username: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    friend = _get_user_by_username(db, username)
    if not friend:
        raise HTTPException(404, "User not found")
    a, b = _friend_pair(current_user.id, friend.id)
    row = db.query(Friendship).filter(Friendship.user_a_id == a, Friendship.user_b_id == b).first()
    if row:
        db.delete(row)
        db.commit()
    return {"ok": True}

@app.post("/api/friends/block")
def block_user(body: FriendBody, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    target = _get_user_by_username(db, body.username)
    if not target:
        raise HTTPException(404, "User not found")
    if target.id == current_user.id:
        raise HTTPException(400, "You cannot block yourself")

    # Remove friendship and pending requests in both directions.
    a, b = _friend_pair(current_user.id, target.id)
    friendship = db.query(Friendship).filter(Friendship.user_a_id == a, Friendship.user_b_id == b).first()
    if friendship:
        db.delete(friendship)
    pending = db.query(FriendRequest).filter(
        or_(
            (FriendRequest.from_user_id == current_user.id) & (FriendRequest.to_user_id == target.id),
            (FriendRequest.from_user_id == target.id) & (FriendRequest.to_user_id == current_user.id)
        )
    ).all()
    for req in pending:
        db.delete(req)

    existing = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == current_user.id,
        BlockedUser.blocked_id == target.id
    ).first()
    if not existing:
        db.add(BlockedUser(blocker_id=current_user.id, blocked_id=target.id))
    db.commit()
    return {"ok": True}

@app.get("/api/users/search")
def search_users(q: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).filter(
        User.username.ilike(f"%{q}%"),
        User.id != current_user.id
    ).limit(10).all()
    return [{"id": u.id, "username": u.username} for u in users]

# ── WebSocket ──
@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str,
                              token: str, db: Session = Depends(get_db)):
    from auth import get_current_user as get_user_from_token
    from jose import jwt, JWTError
    from dotenv import load_dotenv
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_change_this")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, channel, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)

# ── Helpers ──
def _pin_dict(pin: Pin) -> dict:
    return {
        "id": pin.id, "lat": pin.lat, "lng": pin.lng,
        "name": pin.name, "type": pin.type, "group_id": pin.group_id,
        "author": pin.author.username if pin.author else "Unknown",
        "reviews": [
            {"author": r.author.username if r.author else "Unknown",
             "initials": (r.author.username[:2].upper() if r.author else "??"),
             "stars": r.stars, "text": r.text,
             "time": r.created_at.strftime("%b %d")}
            for r in pin.reviews
        ]
    }

def _msg_dict(msg: Message) -> dict:
    return {
        "id": msg.id,
        "author": msg.author.username if msg.author else "Unknown",
        "initials": msg.author.username[:2].upper() if msg.author else "??",
        "text": msg.text,
        "time": msg.created_at.strftime("%I:%M %p"),
        "author_id": msg.author_id
    }
