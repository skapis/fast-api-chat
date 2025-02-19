# FastAPI Real-Time Chat Application

A robust real-time chat application built with FastAPI, MongoDB, and WebSocket, featuring user authentication and role-based access control.

## Features

- 🔐 **Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Admin & Basic User roles)
  - Secure password hashing using bcrypt

- 💬 **Real-Time Chat**
  - WebSocket-based real-time messaging
  - Private chat rooms
  - Message history
  - Real-time message broadcasting

- 👥 **User Management**
  - User registration
  - User profile management
  - Role management
  - User listing (admin only)

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT (JSON Web Tokens)
- **Real-Time Communication**: WebSocket
- **Data Validation**: Pydantic
- **Password Hashing**: Passlib with bcrypt

## Prerequisites

- Python 3.7+
- MongoDB
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-chat-app.git
cd fastapi-chat-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env` file:
```env
DB_URL=mongodb://localhost:27017
DB_NAME=chat_app
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.core:app --reload
```

2. Access the application:
- API Documentation: `http://localhost:8000/docs`
- WebSocket Chat Interface: `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /token` - Get access token
- `POST /users/register` - Register new user

### Users
- `GET /users/me` - Get current user details
- `GET /users/` - List all users (admin only)
- `POST /users/add-role` - Add role to user (admin only)
- `POST /users/remove-role` - Remove role from user (admin only)

### Chat
- `POST /chat/new` - Create new chat room
- `GET /chat/my-chats` - Get user's chat rooms
- `GET /chat/{chat_id}` - Get chat messages
- `POST /chat/{chat_id}` - Send message to chat room
- `WebSocket /ws/chat/{chat_id}` - WebSocket connection for real-time chat

## Project Structure

```
app/
├── auth.py          # Authentication logic
├── config.py        # Configuration and environment variables
├── core.py          # FastAPI application and main routes
├── database.py      # Database connection and collections
├── middleware.py    # Custom middleware (RBAC)
├── models.py        # Pydantic models
├── routers/
│   ├── users.py    # User management routes
│   └── chats.py    # Chat functionality routes
└── websockets/
    └── manager_ws.py # WebSocket connection manager
```

## Security Features

- Secure password hashing using bcrypt
- JWT-based authentication
- Role-based access control
- Input validation using Pydantic models
- Environment variable configuration
- CORS middleware
