# 🔐 Authentication & User Management API

This section describes how to set up authentication, register users, log in, and manage user profiles. These endpoints are required before interacting with the Posts and Comments API.

---

## ⚙️ Setup Process

### 1️⃣ Install Required Packages

```bash
pip install django djangorestframework djangorestframework-authtoken Pillow
```

Ensure the following apps are added to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
]
```

Set the authentication configuration:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 👤 User Model Overview

The application uses a **custom user model** (`CustomUser`) extending Django’s authentication system.

### Key Fields

* `username` – unique identifier for login
* `email` – user email address
* `bio` – optional user description
* `profile_picture` – optional profile image
* `followers` – self-referencing many-to-many relationship

### Computed Fields (Serializer)

* `followers_count` – number of users following this user
* `following_count` – number of users this user follows

These computed fields are read-only and returned in profile responses.

---

## 🔑 Authentication Endpoints

Base URL:

```
/accounts/
```

All endpoints use **Token Authentication**.

---

## 1️⃣ Register a New User

**POST** `/accounts/register/`

This endpoint creates a new user account and automatically generates an authentication token.

### Example Request

```json
{
  "username": "skb",
  "email": "skb@example.com",
  "password": "strongpassword123"
}
```

### Example Response (201 Created)

```json
{
  "id": 1,
  "username": "skb",
  "email": "skb@example.com"
}
```

---

## 2️⃣ Login User

**POST** `/accounts/login/`

Authenticates a user and returns a token to be used for protected endpoints.

### Example Request

```json
{
  "username": "skb",
  "password": "strongpassword123"
}
```

### Example Response (200 OK)

```json
{
  "user": {
    "id": 1,
    "username": "skb",
    "email": "skb@example.com",
    "bio": "",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0
  },
  "token": "2f1c9b7d9e..."
}
```

---

## 3️⃣ User Profile (Retrieve & Update)

**GET / PATCH** `/accounts/profile/`

Returns or updates the authenticated user’s profile.

### Required Header

```http
Authorization: Token <your_token_here>
```

### Example Response (200 OK)

```json
{
  "id": 1,
  "username": "skb",
  "email": "skb@example.com",
  "bio": "Backend developer",
  "profile_picture": null,
  "followers_count": 2,
  "following_count": 5
}
```

### Example PATCH Request

```json
{
  "bio": "Backend developer"
}
```

---

## 🚫 Authentication Errors

### Invalid Credentials

```json
{
  "non_field_errors": ["Invalid username or password"]
}
```

### Unauthorized Access

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

# 📘 Posts & Comments API Documentation

This document describes how to interact with the **Posts** and **Comments** endpoints based on the current Django REST Framework implementation.

---

## 🔐 Authentication

All endpoints require authentication.

**Required headers for every request:**

```http
Authorization: Token <your_token_here>
Content-Type: application/json
```

---

# 📝 Posts API

Base URL:

```
/posts/
```

---

## 1️⃣ List Posts (Authenticated User Only)

**GET** `/posts/`

Returns all posts created by the authenticated user.

### Example Request

```http
GET /posts/
Authorization: Token abc123
```

### Example Response (200 OK)

```json
[
  {
    "id": 1,
    "title": "My First Post",
    "content": "Hello world",
    "author": 2,
    "created_at": "2025-12-13T14:30:00Z",
    "updated_at": "2025-12-13T14:30:00Z"
  }
]
```

---

## 2️⃣ Create Post

**POST** `/posts/api/`

The `author` field is automatically set to the logged-in user.

### Example Request

```json
{
  "title": "Learning DRF",
  "content": "Django REST Framework is powerful"
}
```

### Example Response (201 Created)

```json
{
  "id": 2,
  "title": "Learning DRF",
  "content": "Django REST Framework is powerful",
  "author": 2,
  "created_at": "2025-12-13T15:10:00Z",
  "updated_at": "2025-12-13T15:10:00Z"
}
```

---

## 3️⃣ Retrieve a Single Post

**GET** `/posts/{post_id}/`

Only the owner of the post can retrieve it.

### Example Response (200 OK)

```json
{
  "id": 2,
  "title": "Learning DRF",
  "content": "Django REST Framework is powerful",
  "author": 2,
  "created_at": "2025-12-13T15:10:00Z",
  "updated_at": "2025-12-13T15:10:00Z"
}
```

---

## 4️⃣ Update a Post

**PUT / PATCH** `/posts/{post_id}/`

Only the owner of the post can update it.

### PATCH Example

```json
{
  "content": "Updated content"
}
```

### Example Response

```json
{
  "id": 2,
  "title": "Learning DRF",
  "content": "Updated content",
  "author": 2,
  "created_at": "2025-12-13T15:10:00Z",
  "updated_at": "2025-12-13T15:30:00Z"
}
```

---

## 5️⃣ Delete a Post

**DELETE** `/posts/{post_id}/`

### Response

```
204 No Content
```

---

# 💬 Comments API (Nested Under Posts)

Base URL:

```
/posts/{post_id}/comments/
```

---

## 6️⃣ List Comments for a Post

**GET** `/posts/{post_id}/comments/`

Returns all comments associated with the specified post.

### Example Response (200 OK)

```json
[
  {
    "id": 1,
    "post": 2,
    "author": 3,
    "content": "This is tuff",
    "created_at": "2025-12-13T16:00:00Z",
    "updated_at": "2025-12-13T16:00:00Z"
  }
]
```

---

## 7️⃣ Create a Comment

**POST** `/posts/{post_id}/comments/`

The `author` and `post` fields are automatically assigned by the backend.

### Example Request

```json
{
  "content": "This is tuff"
}
```

### Example Response (201 Created)

```json
{
  "id": 2,
  "post": 2,
  "author": 3,
  "content": "This is tuff",
  "created_at": "2025-12-13T16:05:00Z",
  "updated_at": "2025-12-13T16:05:00Z"
}
```

---

## 8️⃣ Retrieve a Single Comment

**GET** `/posts/{post_id}/comments/{comment_id}`

Only the owner of the comment can retrieve it.

### Example Response (200 OK)

```json
{
  "id": 2,
  "post": 2,
  "author": 3,
  "content": "This is tuff",
  "created_at": "2025-12-13T16:05:00Z",
  "updated_at": "2025-12-13T16:05:00Z"
}
```

---

## 9️⃣ Update a Comment

**PATCH** `/posts/{post_id}/comments/{comment_id}`

Only the owner of the comment can update it.

### Example Request

```json
{
  "content": "Updated comment"
}
```

---

## 🔟 Delete a Comment

**DELETE** `/posts/{post_id}/comments/{comment_id}`

### Response

```
204 No Content
```

---

# 🔎 Filtering, Searching & Ordering

### Posts

* **Search fields:** `title`, `content`, `author__username`
* **Ordering fields:** `created_at`, `updated_at`

### Example

```http
/posts/?search=django&ordering=-created_at
```

---

# 🚫 Error Responses

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden (Ownership Violation)

```json
{
  "detail": "You do not own this comment"
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```

---

# ✅ Summary

* Token-based authentication required
* Posts are user-owned
* Comments are nested under posts
* Ownership enforced for update and delete operations
* Clean and RESTful API structure
