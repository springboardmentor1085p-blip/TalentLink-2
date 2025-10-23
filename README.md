# TalentLink - Backend (Flask + SQLite)
Minimal production-ready backend for TalentLink (freelancer <> client platform).
Includes: users, profiles, projects, proposals, contracts, messages, reviews.

## Quick start
1. Create a virtualenv and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   python app.py
   ```
   The API will be available at `http://localhost:5000/`.

## Authentication
This app uses JWTs. After login you will receive `access_token`.
Include it in requests as: `Authorization: Bearer <token>`.

## Endpoints (Overview)
Base: `http://localhost:5000/api`

### Auth
- `POST /api/auth/register`
  - Body: `{ "username","email","password","role" }`
  - role: `client` or `freelancer`
  - Response: 201
- `POST /api/auth/login`
  - Body: `{ "email","password" }`
  - Response: `{ "access_token": "<jwt>" }`
- `GET /api/auth/me` (protected) - returns basic user info.

### Profiles
- `GET /api/profiles/<user_id>` - public profile
- `POST /api/profiles/` (protected) - create/update profile
  - Body example:
    ```json
    {
      "full_name": "Alice",
      "bio": "Full stack dev",
      "skills": "python, flask, react",
      "hourly_rate": 30,
      "availability": "part-time",
      "location": "Remote"
    }
    ```

### Projects
- `GET /api/projects/` - list projects
- `POST /api/projects/` (protected, client only) - create project
  - Body: `{ "title", "description", "budget", "duration", "skills_required" }`
- `GET /api/projects/<id>` - get project detail

### Proposals
- `POST /api/proposals/<project_id>` (protected, freelancer only)
  - Body: `{ "cover_letter", "proposed_rate" }`
- `GET /api/proposals/project/<project_id>` - list proposals for a project
- `PUT /api/proposals/<proposal_id>/status` (protected, client only)
  - Body: `{ "status": "accepted" | "rejected" }`

### Contracts
- `POST /api/contracts/` (protected, client only)
  - Body: `{ "proposal_id", "start_date", "end_date" }`
- `GET /api/contracts/<id>` (protected)

### Messages
- `POST /api/messages/send` (protected)
  - Body: `{ "receiver_id", "content" }`
- `GET /api/messages/thread/<user_id>` (protected)
  - Get conversation between current user and `<user_id>`

### Reviews
- `POST /api/reviews/` (protected)
  - Body: `{ "contract_id", "rating", "comment" }` (rating integer)

## Notes for Frontend
- Prefix all API calls with `/api`.
- After login save the `access_token` in memory (not localStorage if you can avoid; if using localStorage, be careful).
- Attach Authorization header: `Authorization: Bearer <access_token>`.
- The app is minimal — please add client-side validation and error handling for HTTP 4xx responses.
- For real-time messaging consider adding WebSocket (Flask-SocketIO) or polling every few seconds.

## Upgrading to Production
- Switch to PostgreSQL by setting `DATABASE_URL` environment variable.
- Use Gunicorn + Nginx, enable HTTPS, rotate secrets.
- Add migrations (Flask-Migrate / Alembic).
- Harden JWT (access + refresh tokens), rate-limit endpoints, validate inputs more strictly.

## File map
- `app.py` - app factory and blueprint registration
- `models.py` - SQLAlchemy models
- `routes/` - blueprints for each module
- `requirements.txt` - python deps
