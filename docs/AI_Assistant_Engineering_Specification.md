# AI Assistant Project -- Engineering Specification

## Role

Act as the lead engineer responsible for delivering this project from
design through production-quality implementation.

Optimize for:

-   Successful project completion
-   Engineering quality
-   Maintainability
-   Explicit decision making

rather than maximizing discussion or teaching concepts.

Assume I already understand Python, FastAPI, Docker, LangGraph,
LangChain, JWT authentication, SQL, vector databases, and modern backend
engineering. Avoid explaining fundamentals unless explicitly requested.

------------------------------------------------------------------------

# Project Objective

Build a **production-oriented backend AI Assistant** consisting of two
complementary capabilities:

## 1. Normal Chat

-   Low-latency conversational assistant
-   Tool calling
-   Streaming responses
-   Short-term conversational context
-   Long-term memory

## 2. Deep Research

-   User-triggered research workflow
-   Transparent execution
-   Iterative planning
-   Evidence gathering
-   Coverage evaluation
-   Citation-backed research reports

The project is **backend only**.

Do **not** build any frontend, Gradio application, Streamlit
application, or UI unless explicitly requested later.

Everything should be exposed through backend APIs so that any future
frontend can consume the application without architectural changes.

------------------------------------------------------------------------

# Project Goals

The project exists to build a realistic production-quality AI system
while exploring modern AI engineering practices.

The implementation should emphasize:

-   LangGraph workflows
-   LangChain integrations
-   AI system architecture
-   Production backend engineering
-   Long-term memory
-   Tool calling
-   Deep Research workflows
-   Observability
-   Testing
-   Containerization
-   Maintainability

The objective is **not** to maximize the number of AI features.

Every subsystem must solve a real engineering problem.

------------------------------------------------------------------------

# Product Scope

## Normal Chat

Support:

-   Persistent conversations
-   Streaming responses
-   Tool calling
-   Conversation management
-   Short-term context
-   Long-term memory
-   Authentication
-   Conversation history

## Deep Research

Deep Research is **not another chatbot**.

It is an asynchronous research workflow capable of:

-   Creating research plans
-   Refining research plans
-   Searching multiple sources
-   Collecting evidence
-   Evaluating research coverage
-   Iterating until sufficient coverage is achieved
-   Producing structured reports with citations

Deep Research is **explicitly initiated by the user**.

The application must never automatically escalate a normal conversation
into Deep Research.

------------------------------------------------------------------------

# Non-Goals

The project intentionally excludes or postpones:

-   Frontend development
-   Browser automation
-   Autonomous action-taking agents
-   Multi-agent orchestration
-   Complex OAuth/OIDC authentication
-   Full OpenAI Deep Research replication
-   Unnecessary framework reimplementation
-   Features that do not materially improve the project

Depth is preferred over breadth.

------------------------------------------------------------------------

# High-Level Architecture

The application is a backend-only AI Assistant exposing REST APIs.

It consists of two complementary execution modes:

-   Normal Chat
-   Deep Research

Both share:

-   Conversations
-   Authentication
-   Tools
-   Long-term memory

but differ in execution model.

------------------------------------------------------------------------

# Conversation Model

The backend owns the complete conversation lifecycle.

A conversation is a first-class application entity.

Clients simply reference conversations and submit messages.

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

Clients should remain intentionally thin.

------------------------------------------------------------------------

# Normal Chat

Normal Chat is implemented as a LangGraph workflow optimized for
responsiveness.

Capabilities include:

-   Streaming
-   Tool calling
-   Conversation continuity
-   Short-term conversational context
-   Long-term memory retrieval

Avoid unnecessary computation.

------------------------------------------------------------------------

# Deep Research

Deep Research is a separate asynchronous workflow optimized for quality
rather than latency.

The workflow should support:

-   Iterative planning
-   Research plan refinement
-   Search
-   Evidence extraction
-   Coverage evaluation
-   Repeated research iterations
-   Structured report generation with citations

Research reports should become persistent conversation artifacts.

------------------------------------------------------------------------

# Memory

The system distinguishes between conversational context and long-term
memory.

## Short-Term Context

Maintains conversational continuity within the active conversation.

## Long-Term Memory

Long-term memory stores **selectively extracted** information expected
to improve future interactions.

Long-term memory should:

-   Be selective rather than exhaustive
-   Be created asynchronously
-   Support semantic retrieval
-   Remain independent of conversation persistence

Conversation history is **not** long-term memory.

------------------------------------------------------------------------

# Persistence

Prefer native LangGraph persistence capabilities wherever appropriate.

**LangGraph owns:**

-   Graph execution state
-   Thread persistence
-   Checkpoints

**Application owns:**

-   Users
-   Conversations
-   Research jobs
-   Application-specific business entities
-   Long-term memory metadata

Avoid recreating infrastructure already provided by LangGraph unless
there is a clear engineering reason.

------------------------------------------------------------------------

# Architectural Principles

-   Backend-first architecture
-   Prefer framework capabilities over custom infrastructure
-   Separate business logic from AI orchestration
-   Prefer composition over unnecessary abstraction
-   Every subsystem must justify its existence
-   Optimize for maintainability
-   Keep engineering decisions explicit
-   Architecture may evolve if implementation reveals a better solution

------------------------------------------------------------------------

# Technology Stack

## Backend

-   Python
-   FastAPI
-   Uvicorn

## AI

-   LangGraph (workflow orchestration)
-   LangChain (AI integrations)

LangGraph is the orchestration layer.

LangChain provides integrations including:

-   Models
-   Tools
-   Embeddings
-   Structured outputs
-   Retrievers
-   Vector integrations

## Models

Support multiple providers through configuration.

Initially prioritize **Google Gemini** to minimize development costs.

The architecture should allow switching model roles (chat, research,
utility) to providers such as OpenAI without changing business logic.

## Storage

-   PostgreSQL
-   Redis

Use LangGraph persistence where appropriate.

## Background Jobs

Use **ARQ** with Redis for:

-   Deep Research
-   Memory extraction
-   Future asynchronous workloads

## Authentication

Simple JWT bearer authentication.

## Configuration

Use **Pydantic Settings**.

## Observability

Observability consists of distinct subsystems with different responsibilities.

### Application Logging

- Structured logging using `structlog`.
- Human-readable console output in development.
- JSON output in production.

### Audit Logging

- Persistent audit records stored in PostgreSQL.
- Business events only.
- Not implemented through the application logger.

### AI Tracing

- LangSmith for LLM, tool, graph, and prompt execution.
- Independent from application logging.

### Infrastructure Logging

- Uvicorn, SQLAlchemy, Redis, ARQ, and other runtime components integrate into the application's logging configuration.

## Testing

Use:

-   pytest
-   FastAPI testing tools

Include both traditional backend tests and AI evaluation where
appropriate.

## Dependency Management

Use **uv**.

## Containerization

Use:

-   Docker
-   Docker Compose

------------------------------------------------------------------------

# Engineering Philosophy

Production-quality engineering practices should be incorporated from the
beginning whenever practical, including:

-   Structured logging
-   Centralized error handling
-   Testing
-   Observability
-   Configuration management
-   Containerization
-   Maintainable project organization

These should evolve alongside the application rather than being deferred
until the end.

------------------------------------------------------------------------

# Decision Transparency

For every non-trivial implementation decision, explicitly state:

-   **Decision**
-   **Reason**
-   **Impact** (if any)

Continue implementation immediately unless the decision materially
changes the agreed architecture, project scope, or previous design
decisions.

Only architectural changes require confirmation.

------------------------------------------------------------------------

# Framework-First Principle

Before implementing custom infrastructure, determine whether LangGraph
or LangChain already provides a production-ready solution.

Prefer extending framework primitives over building equivalent
infrastructure.

Custom implementations should exist only when:

-   Framework capabilities are insufficient
-   Application-specific behavior is required
-   There is a clear engineering benefit

------------------------------------------------------------------------

# Architecture Evolution

Treat this specification as the project's baseline rather than an
immutable contract.

If implementation reveals a significantly better solution:

1.  Explicitly state the proposed change.
2.  Explain why it is superior.
3.  Explain the impact.
4.  Continue only after confirmation if the architecture changes.

Avoid silently changing architectural decisions.

------------------------------------------------------------------------

# Vertical Slice Development

Implement the project as a sequence of vertical slices.

Each slice should:

-   Leave the project runnable
-   Integrate with existing functionality
-   Include appropriate tests
-   Conclude with meaningful Git commits

Avoid implementing isolated infrastructure that cannot yet be exercised.

------------------------------------------------------------------------

# Git Workflow

-   Initialize Git from the beginning
-   Create small, meaningful commits
-   Finish each vertical slice with logical commits
-   Use commit messages that describe completed work

------------------------------------------------------------------------

# Working Style

Implementation-first.

Avoid unnecessary architectural discussions.

Recommend one reasonable solution rather than presenting many
alternatives.

When multiple reasonable approaches exist:

-   Recommend one
-   Explain why briefly
-   Proceed

Only pause when a decision materially affects architecture or project
scope.

------------------------------------------------------------------------

# During Implementation

Focus on the current vertical slice.

Avoid designing future phases unless they directly influence the current
implementation.

If a future concern materially affects the current implementation, make
the dependency explicit, resolve it, and continue.

------------------------------------------------------------------------

# Final Objective

Deliver a cohesive, production-oriented AI Assistant that demonstrates
modern AI engineering practices through a realistic implementation.

Optimize for:

-   Successful project completion
-   Engineering quality
-   Maintainability
-   Explicit decision making
-   Production readiness

Do **not** optimize for maximizing feature count or demonstrating every
possible AI engineering concept.
