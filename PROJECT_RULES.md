# Project Context & Rules

## Tech Stack
Client: React 18 + Tailwind CSS  
Server: Python 3.12 + FastAPI  
Database: PostgreSQL (SQLAlchemy async)

## Goal
Build a scalable emotion-learning system using a clean client-server architecture.

## Architecture Rules
- Client handles UI only.
- Server handles business logic and database access.
- REST API communication only.
- Modular and scalable folder structure.

## Style Guide
- Client: Functional components, hooks only.
- Server: Async/Await, type hints required.

## Server Architecture Rules (FastAPI)

## Tech Stack
- Python 3.12
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Pydantic v2

---

## General Principles
- Server is fully independent from the Client.
- Server exposes REST API only.
- No UI logic, no HTML rendering.
- All logic is async/await.
- Type hints are mandatory everywhere.

---

## Layered Architecture (Mandatory)

The server must follow a strict layered architecture:

### 1. Routers (API Layer)
- Handle HTTP requests and responses only.
- No business logic.
- No database access.
- Responsible for:
  - Input validation (via Pydantic schemas)
  - Calling service layer
  - Returning responses

Location:
