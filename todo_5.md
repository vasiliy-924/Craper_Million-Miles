## Auth Plan

### 1. Add dependencies
You’ll need packages for:

- password hashing
- JWT creation/validation
- FastAPI OAuth2 bearer extraction

Typical choices:

- `passlib[bcrypt]` or `pwdlib`
- `python-jose[cryptography]` or `PyJWT`

Since your stack note already mentions `python-jose`, use that.

## 2. Create auth-related files
Recommended files:

- `backend/app/core/security.py`
- `backend/app/schemas/auth.py`
- `backend/app/api/routes/auth.py`
- `backend/app/services/auth.py`
- optionally `backend/app/api/deps.py`

## 3. Implement password hashing
In `backend/app/core/security.py` add helpers:

- `hash_password(password: str) -> str` ✅
- `verify_password(plain_password: str, hashed_password: str) -> bool` ✅

Goal:

- store only password hash in DB
- never store raw password

## 4. Implement JWT helpers
In the same `security.py`, add:

- `create_access_token(subject: str | int) -> str` ✅
- `decode_access_token(token: str) -> dict` ✅

JWT should include at least:

- `sub` = user id or username
- `exp` = expiration time

Use values from config:

- `settings.jwt_secret`
- `settings.jwt_algorithm`
- `settings.access_token_expire_minutes`

## 5. Create auth schemas
In `backend/app/schemas/auth.py` add:

- `LoginRequest`
  - `username: str`
  - `password: str`
- `TokenResponse`
  - `access_token: str`
  - `token_type: str = "bearer"`

Optionally also:

- `TokenPayload`
- `CurrentUserResponse`

## 6. Create auth service layer
In `backend/app/services/auth.py` add logic for:

- `authenticate_user(db, username, password)`
- fetch user by username
- verify password hash
- return user if valid, else `None`

This keeps route handlers thin.

## 7. Seed default user
You need one initial user:

- username: `admin`
- password: `admin123`

Best approach for this test:

- create a small seed script, for example `backend/scripts/seed_admin.py`
- it should:
  - open DB session
  - check whether `admin` already exists
  - if not, create it with hashed password

Do **not** hardcode plain password into the DB model or migration.

## 8. Add `POST /auth/login`
Create `backend/app/api/routes/auth.py`

Flow:

1. receive `username` and `password`
2. call auth service
3. if invalid, return `401 Unauthorized`
4. if valid, return JWT token

Response shape:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

## 9. Register auth router
Update central API router to include:

- `auth.router`

Then your backend will expose:

- `POST /auth/login`
- existing `GET /health`

## 10. Add bearer-token dependency
Create a dependency that:

- reads bearer token from `Authorization: Bearer <token>`
- decodes JWT
- loads user from DB
- returns current user
- raises `401` if invalid/expired

Best place:

- `backend/app/api/deps.py`

Typical helper names:

- `oauth2_scheme`
- `get_current_user`

## 11. Protect car endpoints
Later, when you add car routes:

- `GET /cars`
- `GET /cars/{id}`

attach `Depends(get_current_user)` so only authenticated users can access them.

For now, you can prepare the dependency even before car routes exist.

## 12. Suggested implementation order
Do it in this order:

1. `security.py`
2. `schemas/auth.py`
3. `services/auth.py`
4. `api/routes/auth.py`
5. router registration
6. seed script for `admin`
7. run seed script
8. test login manually
9. add `get_current_user`
10. use it on future car routes

## 13. Definition of done for `TODO.md:84-92`
This block is complete when:

- password hashing works
- JWT creation/validation works
- `POST /auth/login` returns token for `admin/admin123`
- invalid credentials return `401`
- default admin user is seeded
- auth dependency for bearer token exists
- car endpoints are ready to be protected with it

## 14. Manual test flow
Once implemented, test this sequence:

1. run backend
2. seed admin user
3. call `POST /auth/login` with:
   - `username: admin`
   - `password: admin123`
4. confirm token is returned
5. call a protected endpoint with no token -> expect `401`
6. call it with valid token -> expect success

## 15. Practical advice
For this test task:

- use username login only
- use access token only, no refresh token
- no signup/registration
- no OAuth
- no RBAC beyond a single admin user

That keeps the auth scope exactly right.

If you want, I can next give you the exact file-by-file content structure for:
- `security.py`
- `schemas/auth.py`
- `services/auth.py`
- `routes/auth.py`
- `deps.py`