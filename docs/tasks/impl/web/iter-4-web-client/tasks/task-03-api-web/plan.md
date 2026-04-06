# Task 03: API for web — plan

**Iteration:** iter-4-web-client

## Goal

Extend the backend HTTP API so the web client can list learning data and support guardian (parent) views: conversations, knowledge snapshots, and guardian-centric routes.

## Scope

- **Conversations:** `GET` endpoint(s) to list conversations for the current user context.
- **Knowledge snapshots:** `GET` endpoint(s) to list knowledge snapshots (history/progress inputs for the UI).
- **Guardian links router:**  
  - List linked children.  
  - Per-student **activity** and **progress** for guardians.

## Out of scope

Web UI; auth mechanics (Task 02) except wiring routes behind existing auth.
