# API Documentation for OpenAuthGuard UserHub

This document provides details of all the API endpoints available in the OpenAuthGuard UserHub service.

---

## Table of Contents

- [API Documentation for OpenAuthGuard UserHub](#api-documentation-for-openauthguard-userhub)
  - [Table of Contents](#table-of-contents)
  - [Health Check](#health-check)
    - [**GET** `/health`](#get-health)
  - [Authentication](#authentication)
    - [Register User](#register-user)
    - [**POST** `/register`](#post-register)
  - [User Management](#user-management)
    - [Get User by ID](#get-user-by-id)
    - [**GET** `/users/{user_id}`](#get-usersuser_id)
    - [Get User by Username](#get-user-by-username)
    - [**GET** `/users/username/{username}`](#get-usersusernameusername)
    - [Update User](#update-user)
    - [**PUT** `/users/{user_id}`](#put-usersuser_id)

---

## Health Check

### **GET** `/health`

**Description**: Check the status of the service and its database connection.

**Response**:

- `200 OK`

  ```json
  {
    "status": "up",
    "database": "connected",
    "version": "0.0.1"
  }
  ```

- `503 Service Unavailable`

```json
{
  "status": "down",
  "database": "not connected",
  "version": "0.0.1"
}
```

---

## Authentication

### Register User

### **POST** `/register`

**Description**: Register a new user.

**Request Body**:

```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "address": "123 Main St",
  "phone_number": "1234567890",
  "role": "user",
  "social_links": {
    "twitter": "https://twitter.com/johndoe"
  }
}
```

**Response**:

- `201 Created`

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "johndoe",
  "email": "johndoe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "address": "123 Main St",
  "phone_number": "1234567890",
  "social_links": {
    "twitter": "https://twitter.com/johndoe"
  },
  "created_at": "2025-01-17T10:00:00Z",
  "updated_at": "2025-01-17T10:00:00Z"
}
```

- `400 Bad Request`

```json
{
  "detail": "Email is already registered."
}
```

---

## User Management

### Get User by ID

### **GET** `/users/{user_id}`

**Description**: Retrieve details of a user by their unique ID.

**Path Parameter**:

- `user_id` (string, required): The unique ID of the user.

**Response**:

- `200 OK`

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "johndoe",
  "email": "johndoe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "address": "123 Main St",
  "phone_number": "1234567890",
  "social_links": {
    "twitter": "https://twitter.com/johndoe"
  },
  "created_at": "2025-01-17T10:00:00Z",
  "updated_at": "2025-01-17T10:00:00Z"
}
```

- `404 Not Found`

```json
{
  "detail": "User not found."
}
```

---

### Get User by Username

### **GET** `/users/username/{username}`

**Description**: Retrieve details of a user by their unique username.

**Path Parameter**:

- `username` (string, required): The username of the user.

**Response**:

- `200 OK`  
  Same as [Get User by ID](#get-user-by-id).
- `404 Not Found`

```json
{
  "detail": "User not found."
}
```

---

### Update User

### **PUT** `/users/{user_id}`

**Description**: Update details of an existing user.

**Path Parameter**:

- `user_id` (string, required): The unique ID of the user.

**Request Body**:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "address": "456 Another St",
  "phone_number": "9876543210",
  "social_links": {
    "linkedin": "https://linkedin.com/in/johndoe"
  }
}
```

**Response**:

- `200 OK`  
  Same as [Get User by ID](#get-user-by-id).
- `404 Not Found`

```json
{
  "detail": "User not found."
}
```
