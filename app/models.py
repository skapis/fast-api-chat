import uuid
from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from typing import Optional
from bson import ObjectId
from datetime import datetime as dt

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class RolesEnum(str, Enum):
    admin = "admin"
    user = "basic_user"

class Role(BaseModel):
    role_id: str = Field(description="Unique identifier for the role", default_factory=lambda: str(uuid.uuid4()))
    role_name: RolesEnum

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class User(BaseModel):
    id: str = Field(alias="_id", description="Unique identifier of user in db",
                    default_factory=lambda: str(ObjectId()),)
    user_id: str = Field(description="Unique identifier for the user", default_factory=lambda: str(uuid.uuid4()))
    username: str
    hashed_password: str
    roles: Optional[List[Role]] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Chat(BaseModel):
    id: str = Field(alias="_id", description="Unique identifier of chat in db",
                    default_factory=lambda: str(ObjectId()),)
    chat_id: str = Field(description="Unique identifier for the chat", default_factory=lambda: str(uuid.uuid4()))
    users: List[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Message(BaseModel):
    id: str = Field(alias="_id", description="Unique identifier of message in db",
                    default_factory=lambda: str(ObjectId()),)
    message_id: str = Field(description="Unique identifier for the message", default_factory=lambda: str(uuid.uuid4()))
    content: str
    sender: str
    chat_id: str
    sent_at: Optional[str] = Field(default_factory=lambda: str(dt.now()))

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
