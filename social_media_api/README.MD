# Social Media API

## Authentication & User Management

### Setup

1. Clone the repository and navigate into the project directory.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:

   ```bash
   python manage.py migrate
   ```
5. Create a superuser (optional):

   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:

   ```bash
   python manage.py runserver
   ```

---

### User Model Overview

The project uses a custom user model (`CustomUser`) with the following key fields:

* `username`
* `email`
* `bio`
* `profile_picture`
* `followers` (Many-to-Many)
* `following` (Many-to-Many)

Additional computed fields returned via the API:

* `followers_count`
* `following_count`

---

### Authentication Endpoints

#### Register

**Endpoint**

```
POST /accounts/register/
```

**Request Body**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

#### Login

**Endpoint**

```
POST /accounts/login/
```

**Request Body**

```json
{
  "username": "john_doe",
  "password": "password123"
}
```

**Response**

```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0
  },
  "token": "abc123token"
}
```

---

#### Profile

**Endpoint**

```
GET /accounts/profile/
PUT /accounts/profile/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "bio": "Hello world",
  "profile_picture": null,
  "followers_count": 3,
  "following_count": 5
}
```

---

## Posts & Comments API

> All endpoints below require authentication.

---

### Posts

#### List Posts

```
GET /posts/
```

**Response**

```json
[
  {
    "id": 1,
    "title": "My first post",
    "content": "Hello API",
    "author": 1,
    "created_at": "2025-01-01T10:00:00Z"
  }
]
```

---

#### Create Post

```
POST /posts/
```

**Request Body**

```json
{
  "title": "New Post",
  "content": "This is my content"
}
```

---

#### Retrieve / Update / Delete Post

```
GET    /posts/{id}/
PUT    /posts/{id}/
PATCH  /posts/{id}/
DELETE /posts/{id}/
```

---

### Comments (Nested)

#### List Comments for a Post

```
GET /posts/{post_id}/comments/
```

---

#### Create Comment

```
POST /posts/{post_id}/comments/
```

**Request Body**

```json
{
  "content": "This is a comment"
}
```

---

#### Retrieve / Update / Delete Comment

```
GET    /posts/{post_id}/comments/{id}/
PUT    /posts/{post_id}/comments/{id}/
PATCH  /posts/{post_id}/comments/{id}/
DELETE /posts/{post_id}/comments/{id}/
```

---

## Notes

* Token authentication is required for all protected endpoints
* Users can only modify their own posts and comments
* Filtering, searching, and ordering are supported where applicable
