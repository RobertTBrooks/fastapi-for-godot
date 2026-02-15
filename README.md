# Godot MMO Core Starter

A minimal multiplayer foundation built with **Godot** and **FastAPI**.  
This project provides a clean starting point for developing real-time multiplayer games with:

- Secure username/password authentication
- Encrypted password storage (bcrypt)
- Live WebSocket-based chat
- Real-time MMO-style player position synchronization
- SQLite database persistence

This repository is designed to serve as a stable core framework that can be extended into a full multiplayer game.

---

## Features

### Authentication
- Username/password login
- Password hashing using bcrypt
- Session tracking with `is_active`, `session_id`, and `last_seen`
- Automatic stale-session recovery
- Protection against duplicate active logins

### Real-Time Multiplayer (World Sync)
- WebSocket-based player state updates
- Position and animation synchronization
- Automatic puppet spawning for connected players
- Disconnect handling with cleanup

### Live Chat
- WebSocket chat system
- Real-time broadcast to connected clients
- Username-based message display
- Extensible for chat history and commands

### Database
- SQLite backend
- User state persistence
- Session and heartbeat support

---

## Tech Stack

### Client
- Godot 4.x
- WebSocketPeer
- JSON messaging
- Scene-based player architecture

### Server
- FastAPI
- WebSockets (Starlette)
- SQLite
- bcrypt

---

## Project Structure
Repo for godot
- https://github.com/RobertTBrooks/fastapi-for-godot

res://
├── Scenes/
│   ├── Enemies/
│   ├── Menus/
│   │   ├── Scripts/
│   │   │   ├── chat_manager.gd
│   │   │   ├── login_get_req.gd
│   │   │   ├── login_page.gd
│   │   │   ├── login_post_req.gd
│   │   │   ├── main.gd
│   │   │   ├── puppet_master.gd
│   │   │   └── ws_chat.gd
│   │   ├── Chat_Manager.tscn
│   │   ├── login.tscn
│   │   └── main.tscn
│   ├── Objects/
│   └── Players/
│       ├── Scripts/
│       │   ├── player.gd
│       │   └── puppet.gd
│       ├── player.tscn
│       └── puppet.tscn
├── Scripts/
│   ├── http_get.gd
│   └── http_post.gd
└── icon.svg

FASTAPI-FOR-GODOT/
├── __pycache__/
├── DataBases/
│   ├── db_scripts/
│   │   ├── db_setup.py
│   │   └── db_userdata.py
│   ├── chat_data.db
│   └── userdata.db
├── Routes/
│   ├── __pycache__/
│   ├── chat_ws.py
│   ├── chat.py
│   ├── connected_players.py
│   ├── login.py
│   ├── logout.py
│   └── register.py
├── venv/
├── main.py
└── README.md


---

## Installation

### 1. Clone Repository

```bash
git clone git@github.com:RobertTBrooks/fastapi-for-godot.git
cd fastapi-for-godot
```

---

## Setup Python Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
pip install -r requirements.txt
```

---

## Run FastAPI Server

```bash
uvicorn main:app --reload
```

Server runs at:

- http://127.0.0.1:8000

---

## Run Godot Client

Open the Godot project and run the main scene.

---

## Database Schema

### `userdata` Table

| Column       | Type     | Description                         |
|-------------|----------|-------------------------------------|
| `id`        | INTEGER  | Primary key                         |
| `username`  | TEXT     | Unique username                     |
| `password`  | TEXT     | bcrypt hashed password              |
| `is_active` | INTEGER  | `0` = offline, `1` = active         |
| `session_id`| TEXT     | Current session token               |
| `last_seen` | INTEGER  | Unix timestamp (heartbeat tracking) |

---

## WebSocket Endpoints

### World Sync

**Endpoint**  
`/ws/world/{player_id}`

**Used For**
- Player movement updates  
- Animation state synchronization  
- Puppet spawning and live updates  

**Message Format**
```json
{
  "id": "123",
  "data": {
    "x": 100,
    "y": 200,
    "anim": "run",
    "is_attacking": false
  }
}
```


### Chat

**Endpoint**  
`/ws/chat/{player_id}`

**Message Format**
```json
{
  "type": "chat",
  "username": "robert",
  "id": "123",
  "text": "hello world"
}
```

---

## Security Notes

- Passwords are securely hashed using **bcrypt**
- No plaintext password storage
- Active session tracking prevents duplicate concurrent logins
- WebSocket endpoints can be extended with session validation or token-based authentication

For production use:

- Replace SQLite with PostgreSQL
- Add HTTPS (TLS)
- Implement rate limiting
- Add proper authentication middleware
- Introduce structured logging and monitoring

---

## Roadmap

- Chat history persistence
- Private messaging
- Player inventory system
- Server-side movement validation
- Redis-based scaling
- JWT authentication
- Session key validation for WebSocket authorization

---

## Purpose

This project is intended as a clean, understandable multiplayer foundation rather than a complete game.  
It focuses on clarity, structure, and extensibility.

Use it as a starting point for building a full MMO or multiplayer experience in Godot.

