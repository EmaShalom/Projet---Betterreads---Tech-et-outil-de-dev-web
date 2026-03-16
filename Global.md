## Project Overview

BetterReads is a React 19 + TypeScript + Vite SPA for book recommendations. The frontend lives in `betterreads_web/` and communicates with a REST API backend.

## Commands

All commands run from `betterreads_web/`:

```bash
npm run dev       # Start dev server with HMR
npm run build     # TypeScript check + Vite bundle (outputs to dist/)
npm run lint      # ESLint validation
npm run preview   # Serve production build locally
```

No test framework is configured yet (tests are planned per `DEFINITION_OF_DONE.md`).

**Docker:**
```bash
docker build -t betterreads-web betterreads_web/
docker run -p 8080:80 betterreads-web
```

## Architecture

### Entry Points

- `index.html` → `src/main.tsx` — mounts React with `StrictMode`, `BrowserRouter`, `AuthProvider`, and `App`
- `src/App.tsx` — defines all routes

### Key Layers

| Layer | Location | Purpose |
|-------|----------|---------|
| API client | `src/lib/api.ts` | Axios instance; reads `VITE_API_BASE_URL` env var (default: `http://localhost:8000/api`); auto-injects `Authorization: Bearer` from localStorage |
| Auth | `src/context/AuthContext.tsx` | `useAuth()` hook; token stored under `betterreads_access` / `betterreads_refresh`; user info under `betterreads_user` |
| Pages | `src/pages/` | Route-level components |
| Components | `src/components/` | Reusable UI (`BookCard`, `UserBookCard`, `Layout/`, `SearchBar/`) |
| Styles | `src/index.css`, `src/App.css` | Global reset + layout; no CSS modules |

### API Endpoints in Use

- `POST /auth/token/` — login (field: `username`)
- `POST /auth/register/` — registration
- `GET /users/{id}/livres/` — user's book list (userId currently hardcoded to `2` in `MyBooksPage`)
- `POST /livres/{id}/evaluations/` — submit rating
- `GET /livres/` — all books
- `GET /auteurs/{id}/` — author detail

### Auth Flow

`AuthContext` manages login/register/logout. Components access auth state via `useAuth()`. The axios interceptor in `src/lib/api.ts` handles token injection automatically — no need to set headers manually in pages or components.

## Environment

- `VITE_API_BASE_URL` — backend URL (production: `https://betterreads-api.onrender.com/api`)

## Backend (`betterreads_backend/`)

Django 5 + DRF + SimpleJWT backend. All commands run from `betterreads_backend/`.

### Setup
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # fill in DB credentials
createdb betterreads
python manage.py makemigrations users
python manage.py makemigrations books
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### Apps
- `users/` — `CustomUser` (email as USERNAME_FIELD), register + JWT token endpoints
- `books/` — `Auteur`, `Livre`, `Evaluation`, `UserLivre` models + all API views

### Connect frontend
In `betterreads_web/.env`:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

### JWT note
Frontend sends `{ username: <email>, password }` — simplejwt maps the `username` key to the `email` field automatically.

## Known Issues / TODOs (from DEFINITION_OF_DONE.md)

- `userId` is hardcoded as `2` in `MyBooksPage.tsx` — should use authenticated user's ID
- No test framework configured despite QA requirements
- Several pages are placeholder stubs (Messages, Notifications, Community pages)
