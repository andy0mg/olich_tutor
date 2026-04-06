# Task 02: Backend auth — plan

**Iteration:** iter-4-web-client

## Goal

JWT-based authentication plus one-time codes for the web client: issue and verify tokens, persist disposable codes, expose HTTP endpoints, and wire bot commands for web onboarding.

## Scope

- **JWT:** PyJWT for signing and validation; access/refresh flow aligned with web needs.
- **Storage:** `web_auth_codes` table for one-time login and invite codes.
- **API:** Auth router — login, refresh, `me`, web-code generation, invite-code, accept-invite.
- **Identity:** Dual identity in `deps.py` (e.g. student vs guardian contexts where applicable).
- **Bot:** `/web` and `/invite` commands to surface codes and flows for the web app.

## Out of scope

Frontend implementation (covered in later tasks); unrelated API changes.
