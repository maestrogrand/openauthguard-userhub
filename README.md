# OpenAuthGuard Users Manage Services

UserHub is a FastAPI-based microservice designed for managing individual user accounts. It provides endpoints for user registration, profile management, and authentication. It integrates with a PostgreSQL database and includes secure password handling and JWT-based authentication.

---

## Features

### Core Features

- **User Registration**: Create new user accounts with unique usernames and email addresses.
- **User Profile Management**: Update user details such as first name, last name, address, and phone number.
- **Secure Authentication**:
  - Hashing passwords using bcrypt.
  - JWT-based access token generation and validation.
- **Health Check**: Service and database status verification through a dedicated health endpoint.
- **Role Management**: Assign and manage user roles (`user`, `admin`).
