# TalentLink Backend API Documentation

Welcome to the TalentLink Backend API documentation! This guide will help you understand and use all the available API endpoints in your Flask frontend application.

## Table of Contents
1. [Authentication](#authentication)
2. [User Profiles](#user-profiles)
3. [Projects](#projects)
4. [Proposals](#proposals)
5. [Contracts](#contracts)
6. [Messages](#messages)
7. [Reviews](#reviews)

## Base URL
All API endpoints start with: `http://your-backend-url/api`

## Authentication

### Register a New User
- **Endpoint**: `POST /api/auth/register`
- **Description**: Register a new user (client or freelancer)
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "freelancer"  // or "client"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "registered"
  }
  ```

### Login
- **Endpoint**: `POST /api/auth/login`
- **Description**: Authenticate and get an access token
- **Request Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

### Get Current User Info
- **Endpoint**: `GET /api/auth/me`
- **Description**: Get information about the currently logged-in user
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "freelancer"
  }
  ```

## User Profiles

### Get User Profile
- **Endpoint**: `GET /api/profile/<int:user_id>`
- **Description**: Get profile information for a specific user
- **Success Response**: `200 OK`
  ```json
  {
    "user_id": 1,
    "full_name": "John Doe",
    "bio": "Experienced web developer",
    "skills": "Python, JavaScript, React",
    "hourly_rate": 50.0,
    "availability": "Full-time",
    "location": "New York, USA"
  }
  ```

### Create/Update Profile
- **Endpoint**: `POST /api/profile/`
- **Description**: Create or update the current user's profile
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "full_name": "John Doe",
    "bio": "Experienced web developer",
    "skills": "Python, JavaScript, React",
    "hourly_rate": 50.0,
    "availability": "Full-time",
    "location": "New York, USA"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "profile saved"
  }
  ```

## Projects

### List All Projects
- **Endpoint**: `GET /api/project/`
- **Description**: Get a list of all projects
- **Success Response**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "title": "Website Development",
      "description": "Need a website for my business",
      "budget": 1000.0,
      "duration": "1 month",
      "skills_required": "HTML, CSS, JavaScript",
      "client_id": 1
    }
  ]
  ```

### Create Project (Client Only)
- **Endpoint**: `POST /api/project/`
- **Description**: Create a new project (only for clients)
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "title": "Mobile App Development",
    "description": "Need an iOS and Android app",
    "budget": 5000.0,
    "duration": "3 months",
    "skills_required": "React Native, Node.js"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "project created",
    "id": 2
  }
  ```

### Get Project Details
- **Endpoint**: `GET /api/project/<int:project_id>`
- **Description**: Get details of a specific project
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "title": "Website Development",
    "description": "Need a website for my business",
    "budget": 1000.0,
    "duration": "1 month",
    "skills_required": "HTML, CSS, JavaScript",
    "client_id": 1
  }
  ```

## Proposals

### Submit Proposal (Freelancer Only)
- **Endpoint**: `POST /api/proposal/<int:project_id>`
- **Description**: Submit a proposal for a project (only for freelancers)
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "cover_letter": "I have 5 years of experience in web development...",
    "proposed_rate": 800.0
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "proposal submitted",
    "id": 1
  }
  ```

### List Proposals for a Project
- **Endpoint**: `GET /api/proposal/project/<int:project_id>`
- **Description**: Get all proposals for a specific project
- **Success Response**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "project_id": 1,
      "freelancer_id": 2,
      "cover_letter": "I have 5 years of experience...",
      "proposed_rate": 800.0,
      "status": "pending"
    }
  ]
  ```

### Update Proposal Status (Client Only)
- **Endpoint**: `PUT /api/proposal/<int:proposal_id>/status`
- **Description**: Update the status of a proposal (accept/reject)
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "status": "accepted"  // or "rejected"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "status updated"
  }
  ```

## Contracts

### Create Contract (Client Only)
- **Endpoint**: `POST /api/contract/`
- **Description**: Create a new contract from an accepted proposal
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "proposal_id": 1,
    "start_date": "2025-11-01",
    "end_date": "2025-12-31"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "contract created",
    "id": 1
  }
  ```

### Get Contract Details
- **Endpoint**: `GET /api/contract/<int:contract_id>`
- **Description**: Get details of a specific contract
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "proposal_id": 1,
    "start_date": "2025-11-01",
    "end_date": "2025-12-31",
    "status": "active"
  }
  ```

## Messages

### Send Message
- **Endpoint**: `POST /api/message/send`
- **Description**: Send a message to another user
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "receiver_id": 2,
    "content": "Hi, I'm interested in your project!"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "sent",
    "id": 1
  }
  ```

### Get Message Thread
- **Endpoint**: `GET /api/message/thread/<int:user_id>`
- **Description**: Get message history between current user and another user
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Success Response**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "sender_id": 1,
      "receiver_id": 2,
      "content": "Hi, I'm interested in your project!",
      "timestamp": "2025-10-23T17:30:00"
    },
    {
      "id": 2,
      "sender_id": 2,
      "receiver_id": 1,
      "content": "Great! Let's discuss the details.",
      "timestamp": "2025-10-23T17:32:15"
    }
  ]
  ```

## Reviews

### Create Review
- **Endpoint**: `POST /api/review/`
- **Description**: Submit a review for a completed contract
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "contract_id": 1,
    "rating": 5,
    "comment": "Excellent work, highly recommended!"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "review saved",
    "id": 1
  }
  ```

## Testing the API

### Using cURL
Here's how to test the login endpoint using cURL:

```bash
curl -X POST http://your-backend-url/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "securepassword123"}'
```

### Using Python with requests
```python
import requests

# Login and get token
response = requests.post(
    'http://your-backend-url/api/auth/login',
    json={"email": "john@example.com", "password": "securepassword123"}
)
token = response.json()['access_token']

# Make authenticated request
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://your-backend-url/api/auth/me', headers=headers)
print(response.json())
```

## Error Handling
All error responses follow this format:
```json
{
  "error": "Error message describing the issue"
}
```

Common HTTP status codes:
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Not authorized to perform this action
- `404 Not Found`: Resource not found

## Authentication Flow
1. User registers with email, password, and role (client/freelancer)
2. User logs in to get an access token
3. Include the token in the `Authorization` header for protected routes:
   ```
   Authorization: Bearer <access_token>
   ```
4. The token is valid until it expires (default: 15 minutes)

## Rate Limiting
API requests are rate limited to prevent abuse. If you exceed the limit, you'll receive a `429 Too Many Requests` response.

## Support
For any questions or issues, please contact the development team.
