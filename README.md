# Movie Review Platform

A full-stack **Movie Review Platform** developed as the final project for **Coding Factory 9**.

The application provides a complete environment for browsing movies, searching by multiple criteria, rating and reviewing movies, exploring movie relationships, and managing application data through role-protected administrative functionality.

The project was designed around a domain-oriented model and follows a layered backend architecture with a **Repository Layer**, **Service Layer**, **REST API**, and a separate **React frontend**.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Main Features](#main-features)
- [Architecture](#architecture)
- [Domain Model](#domain-model)
- [Business Rules](#business-rules)
- [Authentication and Authorization](#authentication-and-authorization)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Initial Application Data](#initial-application-data)
- [Running in Development](#running-in-development)
- [Building the Application](#building-the-application)
- [Production Deployment](#production-deployment)
- [Updating an Existing Deployment](#updating-an-existing-deployment)
- [Security Notes](#security-notes)
- [License](#license)

---

# Project Overview

The Movie Review Platform is a full-stack web application built with:

- **FastAPI** for the backend REST API
- **React and TypeScript** for the frontend
- **PostgreSQL** for persistent data storage
- **SQLModel / SQLAlchemy** for database access and object-relational mapping
- **Alembic** for database migrations
- **JWT-based authentication** for protected application access

The application is structured so that database access, business logic, HTTP handling, API validation, and frontend presentation remain separated.

The main domain consists of:

- Users
- Movies
- Reviews
- Actors
- Directors
- Genres

The application also implements authentication, authorization, administrative user management, movie management, review management, movie search, relationship navigation, and rating-based movie discovery.

---

# Main Features

## Movies

Authenticated users can:

- Browse available movies
- Open detailed movie pages
- View:
  - Title
  - Description
  - Release year
  - Duration
  - Age rating
  - Poster
  - Trailer
  - Genres
  - Actors
  - Directors
  - User reviews
  - Average user rating

Administrators can additionally:

- Create movies
- Update movies
- Delete movies when allowed by the application's business rules

Movies can have multiple:

- Genres
- Actors
- Directors

---

## Movie Search

The dashboard provides movie searching by:

- **Title**
- **Genre**
- **Actor**
- **Director**

Title, actor, and director searches accept text input.

Genre searching uses a dropdown populated from the genres stored in the database. This ensures that the exact genre value expected by the backend is used.

Search results reuse the same movie presentation components as the main movie list.

---

## Ratings

The application contains a dedicated **Ratings** page.

Users can choose between different rating-based views.

### Top Rated Movies

Displays the highest-rated movies according to user reviews.

The user can select the number of results to display:

- Top 5
- Top 10
- Top 20
- Top 50

### Minimum Rating

Allows the user to provide a minimum average rating and displays only movies whose calculated average rating is equal to or greater than that value.

Ratings are calculated from active users' reviews.

---

## Reviews

Authenticated users can:

- Create a review for a movie
- Give a numeric rating from **1 to 10**
- Add an optional comment
- Update their own review
- Delete their own review

Review ownership is enforced by the backend.

Users cannot edit or delete reviews created by other users.

---

## Actors, Directors and Genres

Movie relationships are directly navigable from the user interface.

Users can:

- Open an actor page and view related movies
- Open a director page and view related movies
- Open a genre page and view movies belonging to that genre

These pages use the relationships defined by the domain model and the corresponding REST API endpoints.

---

## User Accounts

Users can:

- Register
- Log in
- Access protected application pages
- Update account information
- Change their password
- Deactivate their own account

Deactivated accounts cannot log in.

---

## Administration

Administrators have access to protected functionality for both movies and users.

### Movie Administration

Administrators can:

- Create movies
- Edit movies
- Delete eligible movies

### User Administration

Administrators can:

- View application users
- Update usernames and email addresses
- Reset passwords
- Activate accounts
- Deactivate accounts
- Grant administrator privileges
- Remove administrator privileges

Administrator functionality is protected at both the frontend and backend levels.

---

# Architecture

The backend follows a layered architecture.

```text
React Frontend
      |
      | HTTP / REST
      v
FastAPI Routes
      |
      v
Service Layer
      |
      v
Repository Layer
      |
      v
Domain Models
      |
      v
PostgreSQL
```

## Domain Models

The domain models represent the application's database entities and their relationships.

They are implemented with SQLModel and form the basis of the PostgreSQL database schema.

---

## Schemas

Pydantic / SQLModel schemas define:

- API request data
- API response data
- Create operations
- Update operations
- Public representations

This separates the public API contract from the database models.

---

## Repository Layer

Repositories are responsible for direct database interaction.

They contain operations such as:

- Create
- Read
- Update
- Delete
- Pagination
- Searching
- Relationship queries
- Rating queries

Repositories do not contain HTTP handling logic.

---

## Service Layer

The Service Layer contains the application's business rules.

Services coordinate repositories and enforce rules before data reaches the API layer.

Examples include:

- Duplicate movie prevention
- Duplicate genre prevention
- Relationship validation
- Review ownership rules
- One-review-per-user-per-movie enforcement
- User activation and deactivation rules
- Movie deletion restrictions
- Administrative user management

---

## REST API Layer

FastAPI route modules act as the application's backend controllers.

Routes are responsible for:

- Receiving HTTP requests
- Validating incoming data
- Resolving the authenticated user
- Enforcing authorization
- Calling service functions
- Returning API responses

All application API routes use the prefix:

```text
/api/v1
```

---

## Frontend

The frontend is implemented with React and TypeScript.

It uses:

- TanStack Router for client-side routing
- TanStack Query for server-state management and cache invalidation
- A generated OpenAPI client for backend communication
- Tailwind CSS for styling

The frontend contains protected routes and conditionally displays administrative controls based on the authenticated user's permissions.

Backend authorization remains the authoritative security layer.

---

# Domain Model

The core relationships are:

```text
User
 |
 | 1
 |
 | *
Review
 |
 | *
 |
 | 1
Movie
```

A user can create multiple reviews.

A movie can receive multiple reviews.

Each individual review belongs to exactly one user and one movie.

Movies also participate in several many-to-many relationships:

```text
Movie * ----- * Genre

Movie * ----- * Actor

Movie * ----- * Director
```

---

## User

Represents an application account.

Important responsibilities include:

- Authentication
- Account state
- Administrator privileges
- Review ownership

---

## Movie

Represents the central content entity of the application.

Movies contain descriptive data and relationships with:

- Genres
- Actors
- Directors
- Reviews

---

## Review

Connects a user with a movie.

A review contains:

- Rating from 1 to 10
- Optional comment
- Creation information

---

## Actor

Represents an actor who can participate in multiple movies.

---

## Director

Represents a director who can be associated with multiple movies.

---

## Genre

Represents a movie genre.

Genres can be associated with multiple movies.

---

# Business Rules

The application implements several domain and security rules.

## Movies

- A movie with the same **title and release year** cannot be created twice.
- Movie relationships are validated before creation and update.
- A movie cannot be deleted if **any historical review** exists for it.

---

## Reviews

- A user can submit only **one review per movie**.
- Ratings must be between **1 and 10**.
- A review comment is optional.
- Users can update only their own reviews.
- Users can delete only their own reviews.
- Administrator status does not override review ownership.

---

## Users

- Users are deactivated rather than permanently deleted.
- Deactivated users cannot log in.
- Existing reviews remain stored when an account is deactivated.
- Reviews from inactive users are excluded from public review and rating results.
- Historical data is therefore preserved without exposing inactive-user reviews publicly.

---

## Administration

Public account creation does **not** expose administrator privileges.

The public user creation schema does not allow a user to set:

```text
is_superuser = true
```

Administrator privileges are modified only through protected user update functionality.

This prevents users from granting themselves administrative access during registration.

---

# Authentication and Authorization

Authentication is implemented using JWT access tokens.

The general authentication flow is:

```text
User credentials
      |
      v
Login endpoint
      |
      v
Credential validation
      |
      v
JWT access token
      |
      v
Authorization: Bearer <token>
      |
      v
Protected REST API
```

The backend uses OAuth2 Bearer authentication for protected requests.

Access tokens expire after a configurable period.

The default configured expiration time is:

```text
60 minutes
```

Authorization is enforced independently from authentication.

Administrative API operations require administrator privileges.

The React frontend also protects administrative routes and hides administrative actions from normal users.

The backend remains responsible for final authorization enforcement.

---

# Initial Administrator Security Model

The initial administrator account is created through the same normal user-creation mechanism used by the application's domain logic.

During database initialization:

```text
FIRST_SUPERUSER
FIRST_SUPERUSER_PASSWORD
        |
        v
UserCreate
        |
        v
Regular user account
        |
        v
UserUpdate(is_superuser=True)
        |
        v
Owner / Administrator account
```

The account is **not created directly as an administrator**.

Instead:

1. A normal user account is created.
2. The application creates a protected `UserUpdate`.
3. `is_superuser` is changed to `true`.

The same security principle is used during normal application operation: administrator privileges are controlled through protected administrative update functionality rather than public registration.

---

# Technology Stack

## Backend

- Python 3.14
- FastAPI
- SQLModel
- SQLAlchemy
- Pydantic
- Pydantic Settings
- PostgreSQL
- Psycopg
- Alembic
- JWT authentication
- OAuth2 Bearer authentication
- pwdlib
- uv

---

## Frontend

- React 19
- TypeScript
- Vite
- TanStack Router
- TanStack Query
- React Hook Form
- Zod
- Tailwind CSS
- Radix UI primitives
- Lucide React
- Bun
- Generated OpenAPI client

---

## Database

- PostgreSQL

---

## API Documentation

- OpenAPI
- Swagger UI

---

# Project Structure

```text
movie-review-platform/
│
├── backend/
│   ├── app/
│   │   ├── alembic/
│   │   │   └── versions/
│   │   │
│   │   ├── api/
│   │   │   └── routes/
│   │   │
│   │   ├── core/
│   │   │
│   │   ├── models/
│   │   │   ├── actor.py
│   │   │   ├── director.py
│   │   │   ├── genre.py
│   │   │   ├── links.py
│   │   │   ├── movie.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   │
│   │   ├── repositories/
│   │   │
│   │   ├── schemas/
│   │   │
│   │   ├── services/
│   │   │
│   │   ├── frontend/
│   │   ├── initial_data.py
│   │   └── main.py
│   │
│   ├── alembic.ini
│   └── pyproject.toml
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── client/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── routes/
│   │
│   ├── bun.lock
│   ├── components.json
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# API Documentation

FastAPI automatically generates Swagger / OpenAPI documentation.

When the backend is running locally:

### Swagger UI

```text
http://localhost:8000/docs
```

### OpenAPI Schema

```text
http://localhost:8000/api/v1/openapi.json
```

The OpenAPI schema is also used by the frontend tooling to generate the typed API client.

---

# Prerequisites

Before running the application, install:

- **Git**
- **Python 3.14**
- **uv**
- **PostgreSQL**
- **Bun**

The repository contains:

```text
.python-version
```

which defines Python 3.14 as the project Python version.

Python dependencies are locked through:

```text
uv.lock
```

Frontend dependencies are locked through:

```text
frontend/bun.lock
```

---

# Environment Configuration

Environment files are intentionally excluded from Git because they contain environment-specific configuration and sensitive information.

## Backend Environment

The backend reads its configuration from the root:

```text
.env
```

The main backend settings are:

| Variable | Required | Description |
|---|---|---|
| `PROJECT_NAME` | Yes | Application name used by FastAPI |
| `SECRET_KEY` | Yes | Secret used by the authentication system |
| `DATABASE_URL` | Yes | PostgreSQL connection URL |
| `FIRST_SUPERUSER` | Yes | Email address used for the initial owner account |
| `FIRST_SUPERUSER_PASSWORD` | Yes | Password used for the initial owner account |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | JWT lifetime in minutes; defaults to `60` |
| `FRONTEND_HOST` | No | Allowed frontend CORS origin; defaults to `http://localhost:5173` |
| `FASTAPI_ENV` | No | May be set to `development` for development-specific behavior |

Example development `.env`:

```env
PROJECT_NAME="Movie Review Platform"

SECRET_KEY="replace-with-a-long-random-secret"

DATABASE_URL="postgresql://movie_user:strong_password@localhost:5432/movie_review"

FIRST_SUPERUSER="owner@example.com"
FIRST_SUPERUSER_PASSWORD="replace-with-a-strong-password"

ACCESS_TOKEN_EXPIRE_MINUTES=60

FRONTEND_HOST="http://localhost:5173"

FASTAPI_ENV="development"
```

---

## Frontend Environment

The React API client uses:

```text
VITE_API_URL
```

to determine the backend base URL.

For local development, create:

```text
frontend/.env
```

with:

```env
VITE_API_URL="http://localhost:8000"
```

The generated API client already contains endpoint paths such as:

```text
/api/v1/...
```

Therefore `VITE_API_URL` should point to the backend origin rather than repeating the `/api/v1` prefix.

For production, set `VITE_API_URL` to the public backend origin **before building the frontend**.

Vite environment values are embedded into the production frontend during the build process.

---

# Database Setup

The application uses PostgreSQL.

## 1. Start PostgreSQL

Ensure PostgreSQL is installed and running.

---

## 2. Create a Database

Create:

- A PostgreSQL database
- A database user
- A secure password

The resulting credentials must match `DATABASE_URL`.

Example:

```env
DATABASE_URL="postgresql://movie_user:strong_password@localhost:5432/movie_review"
```

The backend automatically normalizes standard PostgreSQL URLs to use the Psycopg driver.

---

## 3. Install Backend Dependencies

From the repository root:

```bash
uv sync
```

The root `pyproject.toml` defines the backend as a uv workspace member.

Backend dependencies are defined in:

```text
backend/pyproject.toml
```

Resolved versions are stored in:

```text
uv.lock
```

---

## 4. Apply Database Migrations

Move to the backend directory:

```bash
cd backend
```

Apply all migrations:

```bash
uv run alembic upgrade head
```

Alembic reads the application's configured:

```text
DATABASE_URL
```

and applies migrations from:

```text
backend/app/alembic/versions/
```

To inspect the current database migration revision:

```bash
uv run alembic current
```

---

# Initial Application Data

After migrations have been applied to a fresh database, initialize the required application data.

From:

```text
backend/
```

run:

```bash
uv run python -m app.initial_data
```

The initialization process is idempotent with respect to the data it checks before inserting.

It performs two important tasks.

## Owner Account

If the configured `FIRST_SUPERUSER` does not already exist:

1. The account is created through `UserCreate`.
2. The normal user repository creation flow stores the account.
3. A protected `UserUpdate` sets:
   ```text
   is_superuser = true
   ```

This preserves the rule that public user creation cannot grant administrator privileges.

---

## Predefined Genres

The initialization process also inserts the predefined movie genres.

Existing genres are checked before insertion so they are not recreated unnecessarily.

---

# Running in Development

Development runs the backend and frontend as separate processes.

---

## Backend Development Server

Open a terminal and move to:

```bash
cd backend
```

Start FastAPI in development mode:

```bash
uv run fastapi dev
```

The backend is normally available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Frontend Development Server

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
bun install
```

Start Vite:

```bash
bun run dev
```

The frontend is normally available through the URL printed by Vite, typically:

```text
http://localhost:5173
```

For the default local configuration:

```env
VITE_API_URL="http://localhost:8000"
```

and the backend CORS configuration allows:

```env
FRONTEND_HOST="http://localhost:5173"
```

---

# Building the Application

This section describes the production build process.

## Backend

The FastAPI backend is a Python application and does not require compilation.

Install the locked backend dependencies from the repository root:

```bash
uv sync
```

Before starting a deployment, ensure that the database schema is current:

```bash
cd backend
uv run alembic upgrade head
```

For a new database, also initialize application data:

```bash
uv run python -m app.initial_data
```

---

## Frontend Production Build

Move to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
bun install
```

Ensure that:

```text
VITE_API_URL
```

points to the backend URL that the production frontend should use.

Then run:

```bash
bun run build
```

The build script is:

```text
tsc -p tsconfig.build.json && vite build
```

It therefore performs:

1. TypeScript compilation/type validation
2. Vite production bundling

The project's Vite configuration writes the production output to:

```text
backend/app/frontend/
```

A successful build produces output similar to:

```text
backend/app/frontend/
├── index.html
└── assets/
```

The production build has been configured this way so that frontend build artifacts remain together with the backend project structure.

However, the current FastAPI application does **not** mount or serve this directory automatically.

The generated frontend must therefore be served by a static web server or frontend hosting platform.

---

# Production Deployment

The backend and frontend are deployed as separate runtime concerns.

```text
                         ┌─────────────────────────┐
                         │      Web Browser        │
                         └────────────┬────────────┘
                                      │
                     ┌────────────────┴────────────────┐
                     │                                 │
                     v                                 v
          Static React Frontend                 FastAPI REST API
          backend/app/frontend/                 /api/v1/...
                     │                                 │
                     │                                 v
                     │                           PostgreSQL
                     │
                     └── API requests via VITE_API_URL
```

The frontend build may be hosted:

- By a conventional static web server
- Behind a reverse proxy
- By a static hosting platform

The FastAPI backend runs separately and connects to PostgreSQL.

---

## 1. Clone the Repository

On the target system:

```bash
git clone <repository-url>
cd movie-review-platform
```

---

## 2. Install Required Runtime Tools

Install:

- Python 3.14
- uv
- PostgreSQL
- Bun

A production static web server or hosting platform is also required for the React build.

---

## 3. Configure Backend Environment

Create the root:

```text
.env
```

and configure at minimum:

```env
PROJECT_NAME="Movie Review Platform"

SECRET_KEY="<production-secret>"

DATABASE_URL="postgresql://<user>:<password>@<database-host>:5432/<database>"

FIRST_SUPERUSER="<owner-email>"
FIRST_SUPERUSER_PASSWORD="<strong-owner-password>"

FRONTEND_HOST="https://frontend.example.com"
```

Use production-specific values.


---

## 4. Install Backend Dependencies

From the repository root:

```bash
uv sync
```

---

## 5. Prepare the Production Database

Move to:

```bash
cd backend
```

Apply migrations:

```bash
uv run alembic upgrade head
```

For the first deployment of a new database, initialize application data:

```bash
uv run python -m app.initial_data
```

This creates:

- The initial owner account
- Administrator privileges for that owner
- Predefined genres

---

## 6. Start the Backend

From:

```text
backend/
```

run the production FastAPI server:

```bash
uv run fastapi run
```

FastAPI uses the entrypoint configured in:

```text
backend/pyproject.toml
```

as:

```text
app.main:app
```

The production backend should normally be exposed through an HTTPS-capable reverse proxy or hosting environment.

---

## 7. Configure the Production Frontend API URL

Before building the frontend, configure:

```text
VITE_API_URL
```

to point to the public FastAPI backend.

Example:

```env
VITE_API_URL="https://api.example.com"
```

Because Vite embeds environment variables during the build, changing `VITE_API_URL` after the build requires rebuilding the frontend.

---

## 8. Build the Production Frontend

From the repository root:

```bash
cd frontend
bun install
bun run build
```

The resulting production files are written to:

```text
backend/app/frontend/
```

---

## 9. Serve the Frontend

Serve:

```text
backend/app/frontend/
```

using the chosen static web server or hosting platform.

Because the application uses client-side routing, the static server should be configured with an SPA fallback so that frontend routes resolve to:

```text
index.html
```

The static frontend then communicates with FastAPI through the configured:

```text
VITE_API_URL
```

---

## 10. Configure CORS

The backend accepts browser requests from:

```text
FRONTEND_HOST
```

For production, this value must match the actual public frontend origin.

Example:

```env
FRONTEND_HOST="https://movies.example.com"
```

The frontend and backend deployment configuration must therefore agree:

```text
Frontend:
VITE_API_URL=https://api.example.com

Backend:
FRONTEND_HOST=https://movies.example.com
```

---

# Deployment Summary

A fresh production deployment follows this order:

```text
1. Clone repository
        |
        v
2. Configure root .env
        |
        v
3. uv sync
        |
        v
4. PostgreSQL available
        |
        v
5. alembic upgrade head
        |
        v
6. initial_data
        |
        v
7. fastapi run
        |
        v
8. Configure VITE_API_URL
        |
        v
9. bun install
        |
        v
10. bun run build
        |
        v
11. Serve backend/app/frontend as static files
```

---

# Updating an Existing Deployment

For an existing deployment:

```bash
git pull
```

Synchronize backend dependencies:

```bash
uv sync
```

Apply any new migrations:

```bash
cd backend
uv run alembic upgrade head
```

Rebuild the frontend:

```bash
cd ../frontend
bun install
bun run build
```

Restart the production FastAPI process after the backend update.

The static frontend host must serve the newly generated files from:

```text
backend/app/frontend/
```

The initial-data command normally does not need to be rerun for every update unless initialization data needs to be restored or added.

---

# Security Notes

The application applies security controls at multiple levels.

- Environment files are excluded from Git.
- Secret values are not stored in the repository.
- Default placeholder secrets are rejected outside the configured development environment.
- User passwords are stored as hashes rather than plain text.
- JWT access tokens are used for authenticated requests.
- Protected API operations require authenticated users.
- Administrative API operations require administrator privileges.
- Public registration cannot assign administrator privileges.
- User review ownership is enforced by the backend.
- Deactivated users cannot log in.
- Frontend authorization controls are backed by backend authorization checks.
- Production deployments should use HTTPS.

---

# API and Frontend Integration

The frontend client is configured in:

```text
frontend/src/main.tsx
```

using:

```text
VITE_API_URL
```

The generated API client contains the REST endpoint paths and sends requests to the configured backend base URL.

For example:

```text
VITE_API_URL=http://localhost:8000
```

combined with an API endpoint such as:

```text
/api/v1/movies
```

results in:

```text
http://localhost:8000/api/v1/movies
```

---

# Development and Build Verification

During development the application was repeatedly verified through:

- Backend Python compilation checks
- Alembic migration configuration checks
- Frontend TypeScript compilation
- Vite production builds
- Manual functional testing
- Authentication and authorization checks
- Administrative permission checks
- Movie CRUD testing
- Review CRUD testing
- User account management testing
- Search testing
- Rating-view testing
- Actor, Director and Genre relationship navigation

A production frontend build can be verified with:

```bash
cd frontend
bun run build
```

A backend syntax compilation check can be performed with:

```bash
cd backend
uv run python -m compileall app
```

The Python dependency lock can be verified from the repository root with:

```bash
uv lock --check
```

---

# License

This project was initially scaffolded from the **Full Stack FastAPI Template** and was extensively adapted for the Movie Review Platform domain and application requirements.

The repository retains the applicable upstream license notice in the `LICENSE` file.