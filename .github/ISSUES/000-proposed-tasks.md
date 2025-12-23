# Proposed issues

This file lists proposed issues to be created in the repository. You can review and convert each entry into an issue.

1. **Add persistent storage (SQLite + SQLAlchemy)**

- **Description:** Replace in-memory `activities` with a persistent DB (start with SQLite + SQLAlchemy). Add models for Activity, ActivityType (optional), Participant and a migration/seed script that imports sample data from current in-memory state.
- **Acceptance criteria:** API persists across restarts; `/activities` loads from DB; a `scripts/seed_db.py` exists; README includes migration steps.
- **Labels:** enhancement, backend
- **Estimate:** medium

2. **Extend participant model & signup payload**

- **Description:** Extend signup to collect participant details: name, mobile, college, branch (not only email). Use Pydantic models for input validation and update frontend form + client JS to post form data.
- **Acceptance criteria:** POST /activities/{name}/signup accepts JSON body with required fields; server validates and stores extra fields; UI shows participant details.
- **Labels:** enhancement, backend, frontend
- **Estimate:** small

3. **Enforce activity capacity (max participants)**

- **Description:** Prevent signups when activity reaches `max_participants`. Return an informative 400 error and surface a message to the UI.
- **Acceptance criteria:** POST returns 400 once activity full; UI shows message; tests cover edge case.
- **Labels:** bug/enhancement, backend, tests
- **Estimate:** small

4. **Add admin role and dashboard (basic auth)**

- **Description:** Add a protected admin endpoint or small dashboard to manage activities and participants (create/edit/delete activities, list/export participants). Implement simple authentication (e.g., login with password, session cookie or token).
- **Acceptance criteria:** Admin can log in, manage activities, and export participant list; non-admins cannot access admin endpoints.
- **Labels:** enhancement, backend, frontend, auth
- **Estimate:** medium

5. **Add images & optional price fields to activities**

- **Description:** Add `image_url` and `price` fields to activities, optional in DB and UI; include static assets folder and display posters/carousel on the site.
- **Acceptance criteria:** Activities API returns image and price fields; static assets served from `/static`; UI displays gallery/poster where available.
- **Labels:** enhancement, frontend
- **Estimate:** small

6. **Harden input handling & DB access (security)**

- **Description:** Add stronger server-side validation, sanitize inputs, and use prepared statements / ORM for DB queries. Add basic CSRF protection where applicable and unit tests for validation rules.
- **Acceptance criteria:** No direct string interpolation into SQL; validation tests pass; linter/security checks added.
- **Labels:** security, backend, tests
- **Estimate:** medium
