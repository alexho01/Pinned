from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Text, Boolean, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid, datetime

Base = declarative_base()

def new_uuid():
    return str(uuid.uuid4())

# Many-to-many: users in groups
group_members = Table("group_members", Base.metadata,
    Column("group_id", String, ForeignKey("groups.id"), primary_key=True),
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
)

# Many-to-many: friendships
friendships = Table("friendships", Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("friend_id", String, ForeignKey("users.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id            = Column(String, primary_key=True, default=new_uuid)
    username      = Column(String, unique=True, nullable=False, index=True)
    email         = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at    = Column(DateTime, default=datetime.datetime.utcnow)
    groups        = relationship("Group", secondary=group_members, back_populates="members")
    friends       = relationship("User", secondary=friendships,
                                 primaryjoin=id == friendships.c.user_id,
                                 secondaryjoin=id == friendships.c.friend_id)
    pins          = relationship("Pin", back_populates="author")
    reviews       = relationship("Review", back_populates="author")
    messages      = relationship("Message", back_populates="author")

class Group(Base):
    __tablename__ = "groups"
    id         = Column(String, primary_key=True, default=new_uuid)
    name       = Column(String, nullable=False)
    emoji      = Column(String, default="👥")
    color      = Column(String, default="#5aabf5")
    owner_id   = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    members    = relationship("User", secondary=group_members, back_populates="groups")
    pins       = relationship("Pin", back_populates="group")
    messages   = relationship("Message", back_populates="group")

class Pin(Base):
    __tablename__ = "pins"
    id         = Column(String, primary_key=True, default=new_uuid)
    lat        = Column(Float, nullable=False)
    lng        = Column(Float, nullable=False)
    name       = Column(String, nullable=False)
    type       = Column(String, default="other")
    group_id   = Column(String, ForeignKey("groups.id"))
    author_id  = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    group      = relationship("Group", back_populates="pins")
    author     = relationship("User", back_populates="pins")
    reviews    = relationship("Review", back_populates="pin", cascade="all, delete")

class Review(Base):
    __tablename__ = "reviews"
    id         = Column(String, primary_key=True, default=new_uuid)
    pin_id     = Column(String, ForeignKey("pins.id"))
    author_id  = Column(String, ForeignKey("users.id"))
    stars      = Column(Integer, default=5)
    text       = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    pin        = relationship("Pin", back_populates="reviews")
    author     = relationship("User", back_populates="reviews")

class Message(Base):
    __tablename__ = "messages"
    id         = Column(String, primary_key=True, default=new_uuid)
    group_id   = Column(String, ForeignKey("groups.id"), nullable=True)
    dm_to_id   = Column(String, ForeignKey("users.id"), nullable=True)  # null if group msg
    author_id  = Column(String, ForeignKey("users.id"))
    text       = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    group      = relationship("Group", back_populates="messages")
    author     = relationship("User", foreign_keys=[author_id], back_populates="messages")
