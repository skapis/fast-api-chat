from fastapi import APIRouter, HTTPException, Depends
from app.models import User, Role, UserCreate
from app.database import users_collection
from app.auth import get_current_user, hash_password

router = APIRouter()

# router for create a new user
@router.post("/register", response_model=dict)
async def create_user(user: UserCreate):
    # check if user already exists by username
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
        roles=[Role(role_name="basic_user").dict(by_alias=True)]
    )
    users_collection.insert_one(new_user.dict(by_alias=True))
    return {"message": "User created successfully"}

# router for get current user
@router.get("/me", response_model=User)
async def get_user_detail(current_user: dict = Depends(get_current_user)):
    user = await users_collection.find_one({"user_id": current_user["user_id"]})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# router for get list of all users in the system
@router.get("/users", response_model=list[dict], dependencies=[Depends(get_current_user)])
async def get_users():
    users = await users_collection.find({}, {'username':1, '_id':0}).to_list()
    return users