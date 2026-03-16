## Next Plan



## Step 10: Frontend foundation

### Goal
Bootstrap the frontend stack only, not full pages yet.

## Recommended stack
Use:

- `Next.js`
- `TypeScript`
- `Tailwind CSS`
- `TanStack Query`

For auth state, keep it simple:
- token in `localStorage`

That matches your MVP plan.

## What to add

### 1. Initialize frontend app
Create a Next app with TypeScript.

If using App Router, that’s fine.

### 2. Add Tailwind
Set up:
- Tailwind
- global styles
- basic layout shell

### 3. Add TanStack Query
Create:
- `QueryClient`
- provider wrapper
- app-level provider

### 4. Add API configuration
Create a small API layer:

- base API URL from env
- helper for authenticated requests
- login request helper
- cars list fetch helper
- car detail fetch helper

### 5. Add auth state management
Keep it minimal.

Suggested pieces:
- `getToken()`
- `setToken()`
- `clearToken()`
- `isAuthenticated()`

You can later wrap this in context or Zustand, but you do not need that yet.

### 6. Add frontend env
Add something like:

- `NEXT_PUBLIC_API_URL=http://localhost:8000`

### 7. Add base app structure
Suggested early folders:

- `src/app` or `app`
- `src/components`
- `src/lib/api`
- `src/lib/auth`
- `src/providers`

## Recommended implementation order

1. finish step 9 worker modes
2. add `worker` service to Docker Compose
3. initialize `frontend/` with Next + TS
4. add Tailwind
5. add TanStack Query provider
6. add API client helpers
7. add token helpers in `localStorage`
8. verify frontend boots locally

## What not to do yet
Leave these for the next frontend steps:

- login page UI
- cars list page
- detail page
- route protection UI

Those belong after the foundation is in place.

## Very practical order
If you want the smoothest path:

1. `Scheduling` first
2. verify worker can run once and in loop
3. then bootstrap `frontend`
4. then move to `/login`, `/cars`, `/cars/[id]`

If you want, I can next give you:
- an exact plan just for `Step 9`
or
- an exact file/folder plan just for `Step 10 frontend foundation`