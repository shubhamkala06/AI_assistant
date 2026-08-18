# AI Assistant Project --- Engineering Specification

## 1. Role and Working Contract

Act as the lead engineer responsible for delivering this project from
design through production-oriented implementation.

Optimize for:

-   Successful project completion
-   Engineering quality
-   Maintainability
-   Explicit architectural decisions
-   Practical implementation progress

Do not optimize for maximizing discussion, teaching fundamentals, or
feature count.

Assume the developer already understands Python, FastAPI, Docker, SQL,
LangGraph, LangChain, JWT/authentication concepts, vector databases, and
modern backend engineering. Explain fundamentals only when explicitly
requested.

------------------------------------------------------------------------

# 2. Project Objective

Build a production-oriented **backend AI Assistant** with two
complementary capabilities:

1.  **Normal Chat**
2.  **Deep Research**

The application is intentionally **backend-first/backend-only during the
current project scope**. No frontend is to be built unless explicitly
requested later.

All functionality must be exposed through backend APIs so that a future
frontend can consume the system without requiring architectural changes.

The project should demonstrate modern AI/backend engineering through a
realistic implementation rather than by maximizing the number of
technologies or features used.

------------------------------------------------------------------------

# 3. Product Scope

## 3.1 Normal Chat

Normal Chat is the primary near-term product slice.

It should eventually support:

-   Persistent conversations
-   Conversation management
-   Streaming responses
-   Tool calling
-   Conversation continuity
-   Short-term conversational context
-   Long-term memory retrieval
-   Authentication
-   Conversation history

Normal Chat should be optimized for responsiveness and should avoid
unnecessary computation.

It will be implemented as a **LangGraph workflow**.

## 3.2 Deep Research

Deep Research is a separate asynchronous workflow optimized for quality
rather than latency.

It should eventually support:

-   User-triggered research jobs
-   Iterative planning
-   Research-plan refinement
-   Search across multiple sources
-   Evidence extraction
-   Coverage evaluation
-   Repeated research iterations
-   Structured report generation
-   Citations
-   Persistent research reports as conversation artifacts

Deep Research is **explicitly initiated by the user**.

Normal Chat must never automatically escalate into Deep Research.

Deep Research is intentionally deferred until the normal chatbot is
substantially complete.

------------------------------------------------------------------------

# 4. Current Scope and Development Order

The project is being implemented through vertical slices.

The current priority is:

1.  Complete the backend foundation.
2.  Complete authentication and user management.
3.  Establish the AI access boundary/gateway decision.
4.  Build the normal chatbot.
5.  Reach a substantial, usable chatbot implementation.
6.  Revisit deferred authentication features such as password
    reset/forgot-password polish.
7.  Continue into Deep Research.
8.  Add further production-oriented AI capabilities only when they solve
    a real problem.

The frontend remains out of scope for now.

------------------------------------------------------------------------

# 5. Non-Goals

The project intentionally excludes or postpones:

-   Frontend development
-   Gradio/Streamlit UI
-   Browser automation
-   Autonomous action-taking agents
-   Multi-agent orchestration unless later justified
-   Full replication of commercial Deep Research systems
-   Reimplementation of capabilities already provided adequately by
    selected frameworks
-   Features that do not materially improve the application
-   Premature infrastructure introduced only for demonstration purposes

Depth and engineering quality are preferred over breadth.

------------------------------------------------------------------------

# 6. High-Level Architecture

The system is a backend application exposing APIs.

Conceptually:

``` text
Client
  |
  v
FastAPI
  |
  +-----------------------------+
  |                             |
  v                             v
Application Domains         AI Workflows
  |                             |
  |                             +--> Normal Chat (LangGraph)
  |                             |
  |                             +--> Deep Research (LangGraph + background jobs)
  |
  +--> PostgreSQL
  +--> Redis
  +--> Authentication
  |
  v
AI Access Boundary / Gateway
  |
  +--> Model Provider(s)
```

Normal Chat and Deep Research share:

-   Authentication
-   Users
-   Conversations
-   Tools
-   Long-term memory
-   AI model access

but have different execution models.

------------------------------------------------------------------------

# 7. Domain Architecture

Business capabilities are separated into domains.

At the current stage, **Users** and **Auth** are separate domains.

Authentication is not considered part of the Users domain merely because
authentication operates on users.

Conceptually:

``` text
app/
├── api/
│   └── router.py
│
├── core/
│   ├── config.py
│   └── observability/
│
├── domains/
│   ├── users/
│   └── auth/
│
└── infrastructure/
    └── database/
```

Future domains such as conversations, chat, memory, research, and
AI/model access should be introduced when their responsibility becomes
concrete.

Do not create domains merely because a concept exists; each domain must
represent a meaningful business capability.

------------------------------------------------------------------------

# 8. Domain Layering Convention

Within a domain, use the following conventional flow:

``` text
router
   ↓
service
   ↓
repository
   ↓
database
```

This convention is intentional.

It provides predictable locations for responsibilities and makes the
codebase easier to navigate as domains grow.

### Router

Responsible for:

-   HTTP concerns
-   Request/response schemas
-   Dependency injection
-   Authentication/authorization dependencies
-   Calling domain services

Routers should not contain business logic.

### Service

Responsible for:

-   Domain/business operations
-   Orchestration of domain-level work
-   Enforcing business rules
-   Coordinating repositories or integrations

Services are the primary public application-facing interface of a
domain.

### Repository

Responsible for:

-   Persistence operations
-   Database queries
-   Database-specific persistence details

A repository may initially contain only one operation if keeping the
boundary is useful for consistency, but unnecessary repository
abstraction should still be avoided when there is no meaningful
persistence boundary.

### Database

Responsible for:

-   SQLAlchemy engine/session infrastructure
-   ORM mappings
-   Database connectivity
-   Migrations

------------------------------------------------------------------------

# 9. Domain Public APIs

Each domain may expose a controlled public API through `__init__.py`.

The public API is an explicit boundary, not a convenience re-export of
everything in the domain.

## Public API rules

-   Domain **services** are the primary things exposed to other domains.
-   Repositories are not directly exposed as the normal cross-domain
    integration mechanism.
-   Routers are **never** exposed through the domain public API.
-   `app/api/router.py` imports domain routers directly.
-   Internal implementation details should remain internal.
-   Models should not be casually re-exported as a public domain API.
-   Types required for legitimate type-hinting may be exposed when
    necessary.
-   Type-only imports should use `TYPE_CHECKING` where appropriate.
-   `from __future__ import annotations` should generally be used
    together with `TYPE_CHECKING` for deferred annotations and to avoid
    unnecessary runtime imports.
-   Public exports should be deliberate and minimal.

When one domain needs another domain's capability, prefer:

``` text
Domain A service
    ↓
Domain B public service API
```

rather than:

``` text
Domain A
    ↓
Domain B repository
```

This keeps domain boundaries intact.

------------------------------------------------------------------------

# 10. FastAPI Users Integration Boundary

FastAPI Users is an external authentication framework and should not be
allowed to spill arbitrary framework-specific code throughout the Auth
domain.

FastAPI Users integration is grouped under the Auth domain:

``` text
domains/
└── auth/
    └── fastapi_users/
        ├── fastapi_users.py
        ├── authentication.py
        ├── database_adapter.py
        ├── manager.py
        └── ...
```

The exact internal files may evolve, but the principle remains:

> Framework-specific integration code should be grouped by the
> integration it implements rather than scattered across unrelated
> domain files.

The Auth domain's public API should expose application-level
authentication capabilities, not FastAPI Users internals.

------------------------------------------------------------------------

# 11. Authentication

Authentication is implemented using **FastAPI Users** with
application-controlled configuration and database persistence.

Current authentication architecture:

``` text
Authentication
    |
    +--> FastAPI Users
    |
    +--> CookieTransport
    |
    +--> DatabaseStrategy
    |
    +--> PostgreSQL access_tokens
    |
    +--> HTTP-only authentication cookie
```

The application uses database-backed authentication tokens rather than
an application-created stateless JWT as the primary session mechanism.

The current authentication cookie is configured through `AuthSettings`.

Current settings include:

-   Access-token lifetime
-   Cookie name
-   Cookie secure flag
-   Cookie SameSite policy
-   Password-reset token secret
-   Verification token secret
-   OAuth state secret
-   Google OAuth client ID
-   Google OAuth client secret

Sensitive values are supplied through environment variables.

------------------------------------------------------------------------

# 12. Authentication Database Model

The current authentication schema includes:

## Users

The Users table is based on FastAPI Users' SQLAlchemy UUID user table.

Current fields include the standard FastAPI Users fields such as:

-   `id`
-   `email`
-   `hashed_password`
-   `is_active`
-   `is_superuser`
-   `is_verified`

The user table is owned by the Users domain.

## Access Tokens

The Auth domain owns the `access_tokens` table.

It contains:

-   `user_id`
-   `token`
-   `created_at`

The `user_id` column has a foreign key to:

``` text
users.id
```

with:

``` text
ON DELETE CASCADE
```

The database foreign key is the persistence relationship. A SQLAlchemy
ORM `relationship()` is not required merely to have a foreign-key
relationship.

## OAuth Accounts

The Auth domain owns the `oauth_accounts` table.

It contains provider/account information including:

-   `user_id`
-   `id`
-   `oauth_name`
-   `access_token`
-   `expires_at`
-   `refresh_token`
-   `account_id`
-   `account_email`

The `user_id` foreign key references:

``` text
users.id
```

with:

``` text
ON DELETE CASCADE
```

This allows one application user to be associated with an OAuth provider
account.

------------------------------------------------------------------------

# 13. Authentication Features

Completed and verified:

-   User registration
-   Password login
-   Authenticated requests
-   Logout
-   Logout-all
-   HTTP-only authentication cookie
-   Database-backed access tokens
-   Google OAuth/OIDC sign-in
-   OAuth account persistence
-   Google user → application user association
-   OAuth-issued application authentication cookie

Google OAuth was tested end-to-end:

``` text
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

The Google OAuth flow currently terminates at the backend callback with
a successful response.

A frontend-specific post-login redirect is intentionally not implemented
because the project currently has no frontend.

This is considered a complete backend OAuth/OIDC authentication slice.

------------------------------------------------------------------------

# 14. Password Reset and Account Recovery

FastAPI Users password-reset and forgot-password capabilities are
considered useful features and are **not discarded**.

They are currently on hold.

Do not spend project time polishing or debugging these features until
the application reaches a substantial normal-chatbot stage.

After the normal chatbot is substantially complete, revisit:

-   Forgot-password
-   Reset-password
-   Related verification/recovery UX

------------------------------------------------------------------------

# 15. OAuth/OIDC Scope

Google OAuth provides the current external identity provider
integration.

The project has demonstrated a complete OAuth/OIDC sign-in flow using:

-   `httpx-oauth`
-   `GoogleOAuth2`
-   FastAPI Users
-   OAuth state protection
-   Google token exchange
-   Google profile retrieval
-   OAuth account persistence
-   Application authentication cookie issuance

The lack of a frontend redirect destination is a current UX limitation,
not an authentication failure.

Do not introduce custom OAuth callback implementations merely to solve
this temporary backend-only browser UX.

------------------------------------------------------------------------

# 16. Database Infrastructure

Use:

-   PostgreSQL
-   SQLAlchemy
-   SQLAlchemy async sessions
-   `asyncpg`
-   Alembic

Database access is centralized through the infrastructure database
layer.

A reusable database-session dependency is used by application
components.

Conceptually:

``` text
DatabaseSession
    ↓
AsyncSession
    ↓
PostgreSQL
```

Alembic owns schema migrations.

Migrations must be committed as part of the corresponding vertical
slice.

Autogenerated migrations should be reviewed rather than blindly trusted.

------------------------------------------------------------------------

# 17. Redis

Redis is part of the infrastructure stack.

Redis is intended for:

-   FastAPI/application transient state where appropriate
-   Background jobs
-   ARQ
-   Future asynchronous workloads
-   Other explicitly justified ephemeral data

Redis should not be used as a replacement for PostgreSQL when durable
relational persistence is required.

------------------------------------------------------------------------

# 18. Configuration

Use **Pydantic Settings**.

Configuration is grouped by responsibility, currently including:

-   Application settings
-   Logging settings
-   Database settings
-   Authentication settings

Settings are loaded from environment variables and `.env` during
development.

Use computed configuration properties for derived values such as
database URLs.

Do not hard-code secrets, credentials, or environment-specific
configuration.

------------------------------------------------------------------------

# 19. Error Handling

Use centralized application error handling.

Services may allow lower-level/library errors to propagate when
appropriate.

Orchestration/application layers should translate those errors into
application-level errors where the error needs to be exposed through the
API.

Do not expose raw internal/library errors to API consumers.

------------------------------------------------------------------------

# 20. Application Observability

Application observability is distinct from AI tracing and AI gateway
observability.

Current application observability includes:

-   Structured logging using `structlog`
-   Human-readable development logging
-   Centralized exception handling
-   Request logging/middleware
-   Request IDs
-   Request duration
-   HTTP method/path/status
-   Infrastructure/runtime logging integration where appropriate

Application observability answers questions such as:

``` text
Which HTTP request failed?
Which application operation was running?
How long did the request take?
What status was returned?
```

It should remain independent of AI-specific tracing.

------------------------------------------------------------------------

# 21. AI Tracing --- LangSmith

LangSmith is the planned primary AI execution tracing system.

It should be used for:

-   LLM calls
-   Prompts
-   Tool calls
-   LangGraph execution
-   Agent/workflow traces
-   AI execution debugging

LangSmith answers questions such as:

``` text
Why did the agent take this action?
Which tool did it call?
What did the tool return?
Which LLM call produced this intermediate result?
How did the graph execute?
```

LangSmith does **not** replace application observability or LangChain middleware.

LangSmith is an observability/tracing system; LangChain middleware is an execution customization mechanism. They should not be treated as interchangeable.

------------------------------------------------------------------------

# 22. LangChain Middleware and Deep Agents

LangChain middleware and Deep Agents are **potential capabilities to evaluate**, not mandatory architectural components.

They were identified as potentially relevant while exploring the LangChain ecosystem.

## LangChain Middleware

LangChain middleware operates at the AI/agent execution layer and is conceptually different from FastAPI application middleware.

The distinction is:

```text
FastAPI middleware
    -> HTTP/application lifecycle

LangChain middleware
    -> AI/agent execution lifecycle
```

LangChain middleware should be used only when a concrete AI-runtime requirement maps naturally to it. Do not create a generic middleware layer or introduce LangChain middleware merely because the framework provides it.

Its applicability should be evaluated when implementing the relevant AI workflow.

## Deep Agents

LangChain's Deep Agents capabilities may be relevant to the future Deep Research implementation.

Deep Agents should be evaluated when the Deep Research slice is reached rather than being assumed as a mandatory implementation choice.

At that point, determine:

- What the Deep Agent abstraction already provides
- Which capabilities the research workflow actually requires
- Which behavior belongs in application/domain logic
- Whether any LangChain middleware is useful
- Which parts should remain implemented through LangGraph or other existing abstractions

The project should avoid adopting Deep Agents or LangChain middleware purely for framework coverage.

---

# 22. AI Gateway

An AI gateway is considered a strong architectural fit for this project.

The gateway sits between the application and model providers:

``` text
Application
    ↓
AI Gateway
    ↓
Model Provider(s)
```

The gateway is intended to provide a centralized AI access boundary for
concerns such as:

-   Provider abstraction
-   Model routing
-   Authentication to providers
-   Rate limiting
-   Retries
-   Fallbacks
-   Cost tracking
-   Token tracking
-   Provider-level latency
-   Provider errors
-   LLM request logging

The gateway should not replace LangSmith or application observability.

## Observability separation

The intended observability layers are:

``` text
Application Observability
    |
    +--> HTTP
    +--> application services
    +--> database/runtime
    +--> business events

LangSmith
    |
    +--> agent execution
    +--> graph execution
    +--> tools
    +--> prompts
    +--> LLM execution

AI Gateway
    |
    +--> provider
    +--> model
    +--> tokens
    +--> cost
    +--> latency
    +--> retries
    +--> fallback
    +--> provider errors
```

These layers answer different questions and should not be collapsed into
one system.

Where possible, trace/context identifiers should allow correlation
between application traces, agent traces, and gateway/model calls.

## Gateway implementation status

The gateway decision is an **architectural direction, not yet an
implemented slice**.

The current recommendation is to evaluate/use **LiteLLM Proxy** as the
gateway because it fits the project's backend-first architecture and
provides:

-   Multi-provider model access
-   OpenAI-compatible interface
-   Routing
-   Retries/fallbacks
-   Rate limiting
-   Cost tracking
-   Centralized model access

Initial gateway adoption should remain minimal:

``` text
Application
    ↓
LiteLLM Proxy
    ↓
One model provider
```

Do not introduce multi-provider routing or sophisticated fallback
policies until there is a real requirement.

------------------------------------------------------------------------

# 23. AI Model Strategy

The application should support multiple model providers through
configuration and the AI access boundary.

The initial model priority is **Google Gemini** to minimize development
costs.

The architecture should allow model roles such as:

-   Chat
-   Research
-   Utility

to switch providers without changing domain/business logic.

Provider-specific code should not leak into business/domain services.

------------------------------------------------------------------------

# 24. LangChain and LangGraph

## LangGraph

LangGraph is the AI workflow orchestration layer.

Use it for:

-   Normal Chat workflow
-   Deep Research workflow
-   Stateful execution
-   Workflow control flow
-   Checkpointing/persistence where appropriate

## LangChain

LangChain provides AI integrations and reusable AI building blocks,
including:

-   Models
-   Tools
-   Embeddings
-   Structured outputs
-   Retrievers
-   Vector integrations

Do not recreate framework functionality without a clear engineering
reason.

------------------------------------------------------------------------

# 25. Conversation Model

The backend owns the complete conversation lifecycle.

A conversation is a first-class application entity.

Clients reference conversations and submit messages.

The backend is responsible for:

-   Conversation management
-   Context construction
-   LangGraph execution
-   Persistence
-   Streaming
-   Long-term memory
-   Deep Research execution

A conversation may contain:

-   Chat interactions
-   Deep Research jobs
-   Deep Research reports

Research reports become persistent conversation artifacts.

------------------------------------------------------------------------

# 26. Memory

The system distinguishes between conversational context and long-term
memory.

## Short-Term Context

Maintains conversational continuity within the active conversation.

## Long-Term Memory

Stores selectively extracted information expected to improve future
interactions.

Long-term memory should:

-   Be selective rather than exhaustive
-   Be created asynchronously where appropriate
-   Support semantic retrieval
-   Remain independent of conversation persistence

Conversation history is not automatically long-term memory.

------------------------------------------------------------------------

# 27. Persistence Ownership

Prefer native LangGraph persistence capabilities wherever appropriate.

### LangGraph owns

-   Graph execution state
-   Thread persistence
-   Checkpoints

### Application owns

-   Users
-   Conversations
-   Research jobs
-   Application-specific business entities
-   Long-term memory metadata

Do not recreate persistence mechanisms already adequately provided by
LangGraph.

------------------------------------------------------------------------

# 28. Background Jobs

Use **ARQ with Redis** for asynchronous workloads such as:

-   Deep Research
-   Long-term memory extraction
-   Future asynchronous processing

Normal Chat should remain responsive and should not unnecessarily depend
on background jobs.

Deep Research is expected to use background execution because it is
explicitly asynchronous and quality-oriented.

------------------------------------------------------------------------

# 29. External Tool Integration

Tool integrations should be introduced only when they solve a real
product requirement.

LangChain is the current abstraction layer for tools.

If an external integration becomes sufficiently broad or numerous,
evaluate **Model Context Protocol (MCP)** as the standardized
integration boundary rather than accumulating point-to-point custom
integrations.

MCP is not a mandatory subsystem at the current stage.

------------------------------------------------------------------------

# 30. Testing

Use:

-   `pytest`
-   FastAPI testing tools
-   Database integration tests where appropriate
-   AI evaluation where appropriate

Testing should evolve with the application rather than being postponed
until the end.

Each vertical slice should include appropriate tests, but not every
intermediate infrastructure change requires a standalone test if it will
be exercised naturally by the next integrated slice.

------------------------------------------------------------------------

# 31. AI Evaluation

AI systems require evaluation beyond traditional backend tests.

The project should eventually include evaluation for relevant AI
behavior, including areas such as:

-   Correctness
-   Factual correctness
-   Retrieval/research quality
-   Tool-use behavior
-   Response quality
-   Agent/workflow behavior

Evaluation design should distinguish between deterministic backend
correctness and probabilistic model behavior.

Evaluators should be treated as a separate evaluation subsystem rather
than being mixed into normal application business logic.

------------------------------------------------------------------------

# 32. Engineering Conventions

## Imports

-   Keep imports explicit.
-   Avoid broad convenience re-exports.
-   Use domain public APIs intentionally.
-   Use `TYPE_CHECKING` for type-only imports where necessary.
-   Use `from __future__ import annotations` where appropriate to reduce
    runtime annotation dependencies and circular-import pressure.
-   Avoid circular dependencies rather than solving them with arbitrary
    re-exporting.

## Framework integrations

Group framework-specific code according to the integration it performs.

Do not scatter a framework's implementation details across unrelated
domain files.

## Routers

Domain routers are directly imported by `app/api/router.py`.

Do not expose routers through domain `__init__.py` public APIs.

This avoids cyclic dependencies and keeps routing composition at the API
boundary.

## Services

Services are the primary cross-domain application boundary.

Other domains should consume a domain's service API rather than reaching
into its repositories or infrastructure.

------------------------------------------------------------------------

# 33. Vertical Slice Development

Implement the system as a sequence of vertical slices.

Each slice should:

-   Leave the application runnable
-   Integrate with existing functionality
-   Include appropriate tests
-   Produce a meaningful Git commit

Avoid building large isolated infrastructure layers that cannot yet be
exercised.

Current completed major slice:

**Authentication and OAuth**

The next major product slice is the **normal chatbot**.

------------------------------------------------------------------------

# 34. Git Workflow

-   Use Git throughout development.
-   Create small, meaningful commits.
-   Finish each vertical slice with logical commits.
-   Commit migrations with the corresponding schema/application slice.
-   Commit messages should describe completed work.

------------------------------------------------------------------------

# 35. Decision Transparency

For every non-trivial implementation decision, explicitly state:

-   **Decision**
-   **Reason**
-   **Impact**

Continue implementation immediately unless the decision materially
changes:

-   Architecture
-   Project scope
-   Existing design constraints

Architectural changes require explicit confirmation.

Do not silently replace an established architectural decision.

------------------------------------------------------------------------

# 36. Framework-First Principle

Before implementing custom infrastructure, determine whether the
selected framework or library already provides a production-ready
capability.

Prefer extending/composing framework primitives over building equivalent
infrastructure.

Custom implementations should exist only when:

-   Framework capabilities are insufficient
-   Application-specific behavior is required
-   There is a clear engineering benefit
-   The abstraction provides a meaningful architectural boundary

------------------------------------------------------------------------

# 37. Architecture Evolution

This specification is the project's current baseline, not an immutable
contract.

If implementation reveals a significantly better solution:

1.  State the proposed change.
2.  Explain why it is superior.
3.  Explain the impact.
4.  Obtain confirmation when the change materially alters architecture
    or scope.
5.  Update this specification after the decision.

Do not silently change architecture.

------------------------------------------------------------------------

# 38. Current Technology Stack

## Backend

-   Python
-   FastAPI
-   Uvicorn
-   SQLAlchemy async
-   PostgreSQL
-   Redis
-   Alembic
-   Pydantic Settings
-   uv

## Authentication

-   FastAPI Users
-   CookieTransport
-   DatabaseStrategy
-   PostgreSQL access tokens
-   Google OAuth2/OIDC through `httpx-oauth`

## AI

-   LangGraph
-   LangChain
-   Google Gemini initially
-   AI gateway planned; LiteLLM Proxy currently recommended

## Async workloads

-   ARQ
-   Redis

## Observability

-   structlog
-   Centralized application error handling
-   Request observability middleware
-   LangSmith for AI execution tracing
-   AI gateway observability for provider/model-level telemetry once
    implemented

## Containerization

-   Docker
-   Docker Compose

## Testing

-   pytest
-   FastAPI testing tools
-   AI evaluation framework/components as appropriate

------------------------------------------------------------------------

# 39. Engineering Philosophy

Production-oriented engineering practices should evolve alongside the
application.

This includes:

-   Structured logging
-   Centralized error handling
-   Testing
-   Observability
-   Configuration management
-   Database migrations
-   Containerization
-   Maintainable domain organization
-   Explicit integration boundaries
-   Secure authentication
-   Appropriate asynchronous processing

Do not postpone these concerns until the end.

At the same time, do not introduce infrastructure merely because it is
considered "production-grade." Every subsystem must have a justified
role in the current architecture.

------------------------------------------------------------------------

# 40. Final Objective

Deliver a cohesive, production-oriented AI Assistant that demonstrates
modern AI engineering practices through a realistic backend
implementation.

Optimize for:

-   Successful project completion
-   Engineering quality
-   Maintainability
-   Explicit architectural decisions
-   Production-oriented design
-   A substantially complete normal chatbot
-   A well-engineered Deep Research workflow

Do **not** optimize for maximizing feature count or demonstrating every
possible AI technology.
