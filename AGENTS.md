#AGENTS.md

This is the project's living working-state file.

It is intentionally separate from `specification.md` and `AGENTS.md`:

- `specification.md` = detailed, relatively stable product and architecture specification.
- `AGENTS.md` = canonical AI-agent onboarding and working rules.
- `PROJECT_STATE.md` = evolving project state, completed slices, current slice, recent decisions, deferred work, and the immediate next steps.

This file should be updated as meaningful slices and architectural decisions are completed.

---

# Current Status

## Completed major slices

### Authentication

Completed and committed.

Verified:

- Signup
- Password login
- Authenticated request
- Logout
- Logout everywhere
- Database-backed access tokens
- HTTP-only authentication cookie

### Google OAuth/OIDC

Completed and committed as a backend authentication integration.

Verified end-to-end:

```text
Application
    ↓
Google authorization
    ↓
Google callback
    ↓
Google token exchange
    ↓
Google profile retrieval
    ↓
User/OAuthAccount persistence
    ↓
Database access token
    ↓
HTTP-only auth cookie
```

Current backend-only behavior:

```text
Google
    ↓
/auth/google/callback
    ↓
204 No Content
```

This is acceptable for the current backend-only stage. A frontend-specific final redirect can be addressed when a frontend exists.

### Authentication architecture

Current domain separation:

```text
domains/
├── auth/
└── users/
```

Auth owns authentication-specific persistence such as:

```text
access_tokens
oauth_accounts
```

Users owns:

```text
users
```

Cross-domain public interaction should primarily happen through services.

---

# Current Slice

## Normal Chat

This is the next major product slice.

The intended direction is:

```text
FastAPI
    ↓
Chat domain/service
    ↓
LangGraph / LangChain
    ↓
LLM gateway
    ↓
Model provider
```

The normal chatbot should become substantially complete before starting Deep Research.

---

# AI Gateway Status

An LLM gateway is currently strongly favored as an architectural boundary.

Current leading candidate:

```text
LiteLLM Proxy
```

Not yet implemented.

Initial adoption should remain minimal:

```text
Application
    ↓
LiteLLM
    ↓
One model provider
```

Do not introduce multi-provider routing, sophisticated fallback policies, or other gateway features unless they solve a real requirement.

The gateway is expected to provide a centralized model-provider boundary for:

- Provider/model routing
- Provider credentials
- Rate limiting
- Retries
- Fallbacks
- Token usage
- Cost tracking
- Provider latency/errors
- LLM request logging

---

# AI Observability

Three observability/runtime boundaries have been identified.

## Application middleware

Current middleware:

- CorrelationIDMiddleware
- AccessLogMiddleware

Responsibility:

```text
HTTP/application lifecycle
```

## LangChain middleware

Potential capability only.

Responsibility:

```text
AI/agent execution lifecycle
```

Do not introduce it unless a concrete AI-runtime requirement makes it useful.

## LLM gateway

Responsibility:

```text
Model/provider boundary
```

Expected telemetry:

- Provider
- Model
- Tokens
- Cost
- Latency
- Retries
- Fallbacks
- Provider errors

## LangSmith

LangSmith remains the planned AI execution tracing layer.

It should help answer:

```text
How did the AI workflow execute?
Why did the agent take an action?
Which tools/model calls were involved?
```

These layers are complementary, not replacements for one another.

---

# Deep Research Status

Deferred.

Do not start Deep Research before Normal Chat is substantially complete.

When the Deep Research slice begins, evaluate LangChain's current Deep Agents capabilities rather than assuming they must be used.

Also evaluate whether LangChain middleware is useful for actual requirements at that point.

Do not adopt framework capabilities simply because they exist.

---

# Deferred Work

## Password reset / forgot password

Useful features.

Intentionally deferred until the normal chatbot reaches a substantial stage.

## Frontend

No frontend currently planned.

Backend-first development continues until the backend/application is substantially complete.

OAuth browser UX that depends on a frontend is therefore deferred.

---

# Architecture Conventions

## Domain layering

Preferred convention:

```text
router
   ↓
service
   ↓
repository
   ↓
database
```

## Public domain APIs

Domains expose deliberate public APIs through `__init__.py`.

Primary cross-domain public interface:

```text
service
```

Repositories are not normally consumed directly across domains.

Routers are not exported through domain public APIs.

`app/api/router.py` imports domain routers directly.

Type-only exports may be exposed when legitimately needed for type hints.

Use:

```python
from __future__ import annotations
```

and `TYPE_CHECKING` where appropriate.

## Framework integrations

Framework-specific code should be grouped by the integration/work it performs.

FastAPI Users integration is grouped under:

```text
app/domains/auth/fastapi_users/
```

Do not scatter FastAPI Users implementation details throughout the Auth domain.

---

# Current Technology Direction

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy async
- PostgreSQL
- Alembic
- Redis
- Pydantic Settings
- uv

## Authentication

- FastAPI Users
- CookieTransport
- DatabaseStrategy
- PostgreSQL access tokens
- Google OAuth/OIDC
- httpx-oauth

## AI

- LangGraph
- LangChain
- Google Gemini initially
- LiteLLM gateway under evaluation/adoption

## Async

- ARQ
- Redis

## AI observability

- LangSmith
- LLM gateway telemetry

## Application observability

- structlog
- FastAPI middleware
- correlation IDs
- access/request logging

---

# Important Database Ownership

```text
Users domain
    └── users

Auth domain
    ├── access_tokens
    └── oauth_accounts
```

Foreign-key relationships exist independently of SQLAlchemy ORM `relationship()` declarations.

For example:

```text
access_tokens.user_id
    → users.id

oauth_accounts.user_id
    → users.id
```

with cascading deletion.

---

# Working Rules for Updating This File

Update this file when:

- A vertical slice is completed
- A major architectural decision is made
- A feature is intentionally deferred
- The next implementation target changes
- A technology is adopted/rejected
- A meaningful domain boundary changes
- A significant integration is completed

Do not record every small implementation action.

Keep this file concise enough to serve as a practical continuation point.

---

# Immediate Next Steps

1. Finalize the AI model-access/gateway boundary for Normal Chat.
2. Implement the Normal Chat slice.
3. Make Normal Chat substantially complete.
4. Revisit deferred password-reset/forgot-password work.
5. Begin Deep Research design and implementation.
6. Evaluate Deep Agents and LangChain middleware when the Deep Research requirements are concrete.
