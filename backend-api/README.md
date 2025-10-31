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

Here’s your **TalentLink API Flow** formatted as a clean, professional `README.md` file for documentation purposes — perfect to include in your backend repo or share with your frontend/Postman team:

---

# 🧩 TalentLink API – Postman Testing Guide

This guide provides a simple and structured way to test the **TalentLink Backend APIs** using **Postman**, with sample requests and responses for both **Clients** and **Freelancers**.

---

## 🚀 Base Configuration

| Key                | Value                   |
| ------------------ | ----------------------- |
| **Base URL**       | `http://127.0.0.1:5000` |
| **Content-Type**   | `application/json`      |
| **Authentication** | JWT Token (Bearer)      |

---

## 🧑‍💼 1. Client Flow

### 1.1 Register Client

**Request**

```http
POST {{base_url}}/api/auth/register
Content-Type: application/json
```

**Body**

```json
{
    "username": "client_user",
    "email": "client@example.com",
    "password": "clientpass123",
    "role": "client"
}
```

**Response**

```json
{
    "message": "registered"
}
```

---

### 1.2 Login Client

**Request**

```http
POST {{base_url}}/api/auth/login
Content-Type: application/json
```

**Body**

```json
{
    "email": "client@example.com",
    "password": "clientpass123"
}
```

**Response**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

> 💡 Save this token as `client_token` in your Postman environment.

---

### 1.3 Create Project

**Request**

```http
POST {{base_url}}/api/projects
Content-Type: application/json
Authorization: Bearer {{client_token}}
```

**Body**

```json
{
    "title": "E-commerce Website",
    "description": "Need a full-stack e-commerce website with payment integration",
    "budget": 2500,
    "duration": "3 months",
    "skills_required": "React, Node.js, MongoDB, Stripe"
}
```

**Response**

```json
{
    "message": "project created successfully",
    "project": {
        "id": 1,
        "title": "E-commerce Website",
        "description": "Need a full-stack e-commerce website with payment integration",
        "budget": 2500.0,
        "duration": "3 months",
        "skills_required": "React, Node.js, MongoDB, Stripe",
        "status": "active",
        "client_id": 1,
        "created_at": "2025-10-24T11:30:00.000000"
    }
}
```

---

### 1.4 View Project Proposals

**Request**

```http
GET {{base_url}}/api/proposals/project/1
Authorization: Bearer {{client_token}}
```

**Response**

```json
[
    {
        "id": 1,
        "project_id": 1,
        "freelancer": {
            "id": 2,
            "username": "dev_expert",
            "email": "dev@example.com"
        },
        "cover_letter": "I have 5+ years of experience with MERN stack...",
        "proposed_rate": 2200.0,
        "status": "pending",
        "created_at": "2025-10-24T11:35:00.000000"
    }
]
```

---

### 1.5 Accept or Reject Proposal

**Request**

```http
PUT {{base_url}}/api/proposals/1/status
Content-Type: application/json
Authorization: Bearer {{client_token}}
```

**Body**

```json
{
    "status": "accepted"
}
```

**Response**

```json
{
    "message": "proposal accepted successfully",
    "proposal_id": 1,
    "status": "accepted"
}
```

---

## 👨‍💻 2. Freelancer Flow

### 2.1 Register Freelancer

**Request**

```http
POST {{base_url}}/api/auth/register
Content-Type: application/json
```

**Body**

```json
{
    "username": "dev_expert",
    "email": "dev@example.com",
    "password": "devpass123",
    "role": "freelancer"
}
```

**Response**

```json
{
    "message": "registered"
}
```

---

### 2.2 Login Freelancer

**Request**

```http
POST {{base_url}}/api/auth/login
Content-Type: application/json
```

**Body**

```json
{
    "email": "dev@example.com",
    "password": "devpass123"
}
```

**Response**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

> 💡 Save this token as `freelancer_token` in your Postman environment.

---

### 2.3 Browse Available Projects

**Request**

```http
GET {{base_url}}/api/projects
Authorization: Bearer {{freelancer_token}}
```

**Response**

```json
[
    {
        "id": 1,
        "title": "E-commerce Website",
        "description": "Need a full-stack e-commerce website with payment integration",
        "budget": 2500.0,
        "duration": "3 months",
        "skills_required": "React, Node.js, MongoDB, Stripe",
        "client_id": 1,
        "status": "active",
        "created_at": "2025-10-24T11:30:00.000000"
    }
]
```

---

### 2.4 Submit Proposal

**Request**

```http
POST {{base_url}}/api/proposals/1
Content-Type: application/json
Authorization: Bearer {{freelancer_token}}
```

**Body**

```json
{
    "cover_letter": "I have 5+ years of experience with MERN stack and have built several e-commerce platforms. I can deliver this project within your timeline.",
    "proposed_rate": 2200.0
}
```

**Response**

```json
{
    "message": "proposal submitted",
    "id": 1,
    "status": "pending",
    "created_at": "2025-10-24T11:35:00.000000"
}
```

---

### 2.5 Check Proposal Status

**Request**

```http
GET {{base_url}}/api/proposals
Authorization: Bearer {{freelancer_token}}
```

**Response**

```json
[
    {
        "id": 1,
        "project": {
            "id": 1,
            "title": "E-commerce Website",
            "budget": 2500.0,
            "status": "active"
        },
        "cover_letter": "I have 5+ years of experience...",
        "proposed_rate": 2200.0,
        "status": "accepted",
        "created_at": "2025-10-24T11:35:00.000000"
    }
]
```

---

## ⚙️ Postman Environment Variables

| Variable           | Description                            |
| ------------------ | -------------------------------------- |
| `base_url`         | API base URL (`http://127.0.0.1:5000`) |
| `client_token`     | Set after client login                 |
| `freelancer_token` | Set after freelancer login             |
| `project_id`       | Auto-set after project creation        |
| `proposal_id`      | Auto-set after proposal submission     |


