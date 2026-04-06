# Task 04: Web auth and routing — plan

**Iteration:** iter-4-web-client

## Goal

Implement client-side authentication, session handling, and route protection so students and parents land on the correct screens after login or invite acceptance.

## Scope

- **Pages:** `LoginPage`, `InvitePage` for credential/code flows.
- **State:** `AuthContext` with JWT storage (memory/localStorage per project convention), login/logout, invite acceptance.
- **Guards:** `RequireAuth` with optional **role** check (student vs parent).
- **Routing:** Role-based route trees — student vs parent areas and nested child routes as specified.

## Out of scope

Full feature screens (Tasks 05–06); backend changes (Tasks 02–03).
