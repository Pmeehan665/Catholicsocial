# Catholic Social Network API

A minimal FastAPI-based prototype for a faith-focused social network. It supports user registration, authentication, posting, and a shared feed using in-memory storage (ideal for demos and local experimentation).

## Features
- **User registration & login** with hashed passwords.
- **Bearer token authentication** for protected routes.
- **Post creation** and a **reverse-chronological feed**.
- **Health check** endpoint for uptime monitoring.

## Quickstart
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the API locally:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Explore the interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## Example Usage
```bash
# Register
curl -X POST http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"username": "peter", "display_name": "St. Peter", "password": "rocksolid"}'

# Login (returns token)
curl -X POST http://localhost:8000/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "peter", "password": "rocksolid"}'

# Create a post
curl -X POST http://localhost:8000/posts \
  -H 'Authorization: Bearer <TOKEN_FROM_LOGIN>' \
  -H 'Content-Type: application/json' \
  -d '{"content": "Welcome to the Catholic social network!"}'

# Fetch the feed
curl http://localhost:8000/feed
```

## Notes
- Data is stored in-memory, so it resets on restart. Swap the storage layer for a database (e.g., PostgreSQL) for production use.
- Tokens are ephemeral and maintained in memory; replace with JWTs or session storage for persistence.
- Passwords are hashed with bcrypt via `passlib`.

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.
