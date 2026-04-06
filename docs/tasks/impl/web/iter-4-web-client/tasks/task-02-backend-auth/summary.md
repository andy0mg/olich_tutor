# Task 02: Backend auth — summary

**Iteration:** iter-4-web-client

## What was done

- Added **PyJWT** for JWT creation and verification.
- Introduced **WebAuthCode** model and **migration 002** for `web_auth_codes`.
- Implemented **JWT service** (issue/refresh/validate as designed for this iteration).
- **Auth endpoints:** login, refresh, `me`, `web-code`, `invite-code`, `accept-invite`.
- **Dual identity** support in `deps.py` for authenticated contexts (student vs guardian).
- **Bot:** `/web` and `/invite` commands integrated with the code and invite flows.

## Status

Done.
