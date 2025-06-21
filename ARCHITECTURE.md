# Task Manager Application Architecture

This document provides a detailed overview of the application architecture and data flow.

## System Architecture

```mermaid
graph TD
    subgraph "Frontend Layer"
        A[Streamlit UI] --> B[API Client]
    end
    
    subgraph "API Layer"
        B --> C[FastAPI Routes]
        C --> D[JWT Authentication]
        C --> E[Pydantic Schemas]
    end
    
    subgraph "Service Layer"
        D --> F[CRUD Operations]
        E --> F
        F --> G[ORM Models]
    end
    
    subgraph "Data Layer"
        G --> H[SQLAlchemy Engine]
        H --> I[SQLite Database]
    end
```

## User Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Streamlit Frontend
    participant Backend as FastAPI Backend
    participant Auth as Auth Service
    participant DB as Database
    
    User->>Frontend: Enter credentials
    Frontend->>Backend: POST /token
    Backend->>Auth: Verify credentials
    Auth->>DB: Query user
    DB-->>Auth: Return user data
    Auth->>Auth: Check password hash
    Auth->>Auth: Generate JWT token
    Auth-->>Backend: Return token
    Backend-->>Frontend: Return token
    Frontend->>Frontend: Store token in session
    Frontend-->>User: Redirect to dashboard
```

## Task Creation Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Streamlit Frontend
    participant Backend as FastAPI Backend
    participant Auth as Auth Service
    participant CRUD as CRUD Service
    participant DB as Database
    
    User->>Frontend: Fill task details & submit
    Frontend->>Frontend: Validate form data
    Frontend->>Backend: POST /tasks/ with JWT
    Backend->>Auth: Verify token
    Auth-->>Backend: User information
    Backend->>CRUD: Create task
    CRUD->>DB: Insert task
    DB-->>CRUD: Confirm insertion
    CRUD-->>Backend: Return task
    Backend-->>Frontend: Return success
    Frontend-->>User: Show success & refresh
```

## Task Listing Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Streamlit Frontend
    participant Backend as FastAPI Backend
    participant Auth as Auth Service
    participant CRUD as CRUD Service
    participant DB as Database
    
    User->>Frontend: View tasks
    Frontend->>Backend: GET /tasks/ with JWT
    Backend->>Auth: Verify token
    Auth-->>Backend: User information
    
    alt is Admin
        Backend->>CRUD: Get all tasks
    else is Regular User
        Backend->>CRUD: Get user's tasks
    end
    
    CRUD->>DB: Query tasks
    DB-->>CRUD: Return tasks
    CRUD-->>Backend: Return tasks
    Backend-->>Frontend: Return tasks
    Frontend->>Frontend: Filter by status (if selected)
    Frontend-->>User: Display tasks
```

## Role-Based Access Control

```mermaid
flowchart TD
    A[Request with JWT] --> B{Validate Token}
    B -- Invalid --> C[Return 401 Unauthorized]
    B -- Valid --> D{Check Role}
    
    D -- Admin --> E[Full Access]
    D -- Regular User --> F[Limited Access]
    
    E --> G[All Tasks]
    E --> H[User Management]
    F --> I[Own Tasks Only]
    F --> J[Profile Management]
```

## Database Schema

```mermaid
erDiagram
    USERS ||--o{ TASKS : creates
    
    USERS {
        int id PK
        string username UK
        string hashed_password
        string role
    }
    
    TASKS {
        int id PK
        string title
        string description
        enum status
        int owner_id FK
    }
```

## Component Dependencies

```mermaid
graph LR
    A[main.py] --> B[auth.py]
    A --> C[crud.py]
    A --> D[schemas.py]
    B --> E[models.py]
    C --> E
    D --> E
    E --> F[database.py]
```

## Data Flow Summary

1. **Authentication Flow**:
   - User logs in via Streamlit frontend
   - Credentials sent to FastAPI backend
   - Backend validates credentials and generates JWT token
   - Token returned to frontend and stored in session state
   - All subsequent requests include the JWT token

2. **Task Management Flow**:
   - Frontend sends requests with JWT token
   - Backend validates token and identifies user
   - Based on user role, appropriate access is granted
   - CRUD operations performed on the database
   - Results returned to frontend for display

3. **Role-Based Access**:
   - Admin users can access all tasks
   - Regular users can only access their own tasks
   - Permissions enforced at the API level