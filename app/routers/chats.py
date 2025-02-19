import json

from fastapi import APIRouter, HTTPException, Depends
from app.models import Chat, Message
from app.database import chats_collection, messages_collection
from app.auth import get_current_user
from app.websockets.manager_ws import manager

router = APIRouter()

# router for create a new chatroom
@router.post("/new", response_model=dict, dependencies=[Depends(get_current_user)])
async def create_chat(username: dict, current_user: dict = Depends(get_current_user)):
    # check if user exists
    chat = await chats_collection.find_one({"users": {"$all": [username["username"], current_user["username"]]}})
    if chat:
        raise HTTPException(status_code=400, detail={
            "message": "Chatroom already exists",
            "chat_id": str(chat["chat_id"])
        })

    # get current user username
    users = [username["username"], current_user["username"]]

    # create chatroom
    chat = Chat(users=users)
    chat_dict = chat.model_dump()
    await chats_collection.insert_one(chat_dict)
    return {"message": "Chatroom created successfully", "chat_id": str(chat_dict["chat_id"])}

# router to get list of all user chats
@router.get("/my-chats", response_model=dict, dependencies=[Depends(get_current_user)])
async def get_my_chats(current_user: dict = Depends(get_current_user)):
    chats = await chats_collection.find({"users": {"$in": [current_user["username"]]}}).to_list(None)
    # return chat_id and users
    chats = [{"chat_id": str(chat["chat_id"]), "users": chat["users"]} for chat in chats]
    return {"chats": chats}


# router to get chat messages
@router.get("/{chat_id}", response_model=dict, dependencies=[Depends(get_current_user)])
async def get_chat_messages(chat_id: str, current_user: dict = Depends(get_current_user)):
    # check if chatroom exists
    chat = await chats_collection.find_one({"chat_id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    # check if user is part of chatroom
    if current_user["username"] not in chat["users"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # get chatroom messages
    messages = await messages_collection.find({"chat_id": chat_id}).to_list(None)
    messages = [{"chat_id": str(message["chat_id"]),
                 "sender": message["sender"],
                 "message_id" : message["message_id"],
                 "sent_at": message["sent_at"],
                 "content": message["content"]} for message in messages]
    return {"messages": messages}

# router to send message to chatroom
@router.post("/{chat_id}", response_model=dict, dependencies=[Depends(get_current_user)])
async def send_message(chat_id: str, message: dict, current_user: dict = Depends(get_current_user)):
    # check if chatroom exists
    chat = await chats_collection.find_one({"chat_id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    # check if user is part of chatroom
    if current_user["username"] not in chat["users"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # create message
    message = Message(chat_id=chat_id, sender=current_user["username"], content=message["message"])
    message_dict = message.model_dump()
    await messages_collection.insert_one(message_dict)

    # broadcast message to all users in specific chatroom
    chat_connections = manager.get_active_connections(chat_id)
    for connection in chat_connections:
        await connection["websocket"].send_text(json.dumps({
            "chat_id": str(message_dict["chat_id"]),
            "sender": message_dict["sender"],
            "message_id": message_dict["message_id"],
            "sent_at": message_dict["sent_at"],
            "content": message_dict["content"]
        }))

    return {"message": "Message sent successfully"}