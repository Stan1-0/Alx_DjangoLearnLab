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

## Follows & Feed API

### User Model Changes

The `CustomUser` model has been extended to support social following functionality.

```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
```

**Key relationships:**

* `user.following.all()` → users this user follows
* `user.followers.all()` → users following this user

---

### Follow a User

**Endpoint**

```
POST /accounts/follow/{user_id}/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
{
  "message": "You are now following john_doe",
  "following_count": 3
}
```

**Note:** When you follow a user, they receive a notification.

---

### Unfollow a User

**Endpoint**

```
POST /accounts/unfollow/{user_id}/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
{
  "message": "You unfollowed john_doe",
  "following_count": 2
}
```

---

### Get Followers List

**Endpoint**

```
GET /accounts/followers/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
[
  {
    "id": 2,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "",
    "profile_picture": null,
    "followers_count": 1,
    "following_count": 0
  }
]
```

---

### User Feed (Posts from Followed Users)

The feed returns posts created by users that the authenticated user follows.

**Endpoint**

```
GET /api/feed/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
[
  {
    "id": 5,
    "title": "A post from someone I follow",
    "content": "This post appears in my feed",
    "author": 2,
    "created_at": "2025-01-10T09:00:00Z"
  }
]
```

---

## Posts & Comments API

> All endpoints below require authentication.

---

### Posts

#### List Posts

```
GET /api/posts/
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
POST /api/posts/
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
GET    /api/posts/{id}/
PUT    /api/posts/{id}/
PATCH  /api/posts/{id}/
DELETE /api/posts/{id}/
```

---

### Likes

#### Like a Post

**Endpoint**

```
POST /api/posts/{id}/like/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
{
  "message": "Post liked successfully."
}
```

**Note:** The post author receives a notification when you like their post.

---

#### Unlike a Post

**Endpoint**

```
POST /api/posts/{id}/unlike/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
{
  "message": "Post unliked successfully."
}
```

---

### Comments (Nested)

#### List Comments for a Post

```
GET /api/posts/{post_id}/comments/
```

---

#### Create Comment

```
POST /api/posts/{post_id}/comments/
```

**Request Body**

```json
{
  "content": "This is a comment"
}
```

**Note:** The post author receives a notification when you comment on their post.

---

#### Retrieve / Update / Delete Comment

```
GET    /api/posts/{post_id}/comments/{id}/
PUT    /api/posts/{post_id}/comments/{id}/
PATCH  /api/posts/{post_id}/comments/{id}/
DELETE /api/posts/{post_id}/comments/{id}/
```

---

## Notifications API

The notification system automatically creates notifications for important user interactions.

### Notification Model

```python
class Notification(models.Model):
    recipient = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
```

**Notifications are automatically created when:**

* Someone follows you
* Someone likes your post
* Someone comments on your post

---

### Get All Notifications

**Endpoint**

```
GET /notifications/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
[
  {
    "id": 1,
    "actor": {
      "id": 2,
      "username": "jane_doe",
      "email": "jane@example.com",
      "bio": "",
      "profile_picture": null
    },
    "verb": "liked your post",
    "target_type": "post",
    "target_id": 5,
    "is_read": false,
    "timestamp": "2025-01-10T14:30:00Z"
  },
  {
    "id": 2,
    "actor": {
      "id": 3,
      "username": "bob_smith",
      "email": "bob@example.com",
      "bio": "",
      "profile_picture": null
    },
    "verb": "started following you",
    "target_type": null,
    "target_id": null,
    "is_read": true,
    "timestamp": "2025-01-09T10:15:00Z"
  }
]
```

**Note:** Unread notifications are displayed first, followed by read notifications.

---

### Get Unread Notifications Only

**Endpoint**

```
GET /notifications/unread/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
[
  {
    "id": 1,
    "actor": {
      "id": 2,
      "username": "jane_doe",
      "email": "jane@example.com",
      "bio": "",
      "profile_picture": null
    },
    "verb": "commented on your post",
    "target_type": "post",
    "target_id": 8,
    "is_read": false,
    "timestamp": "2025-01-10T16:45:00Z"
  }
]
```

---

### Mark Notification as Read

**Endpoint**

```
POST /notifications/{notification_id}/read/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
{
  "message": "Notification marked as read."
}
```

---

### Mark All Notifications as Read

**Endpoint**

```
POST /notifications/read-all/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```json
{
  "message": "5 notifications marked as read."
}
```

---

### Delete a Notification

**Endpoint**

```
DELETE /notifications/{notification_id}/delete/
```

**Headers**

```
Authorization: Token <user_token>
```

**Response**

```
204 No Content
```

---

## Notes

* Token authentication is required for all protected endpoints
* Users can only modify their own posts and comments
* Filtering, searching, and ordering are supported where applicable
* Notifications are automatically created for follows, likes, and comments
* Users cannot follow themselves or like their own posts
* Unread notifications are prominently displayed first in notification lists