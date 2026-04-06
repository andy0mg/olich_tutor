# Task 04: Web auth and routing — summary

**Iteration:** iter-4-web-client

## What was done

- **LoginPage** and **InvitePage** implemented.
- **AuthContext** with JWT-backed session: `login`, `acceptInvite`, `logout`.
- **RequireAuth** guard with **role** validation.
- **Routes:**
  - **Student:** `/`, `/chat/:id`, `/progress`.
  - **Parent:** `/parent`, `/parent/child/:id/*` (nested child routes).

## Status

Done.
