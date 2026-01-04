<!--
Sync Impact Report
==================
Version change: [TEMPLATE] → 1.0.0 (Initial ratification)
Modified principles: N/A (new constitution)
Added sections:
  - Core Principles (8 principles derived from global rules)
  - Development Standards (5 additional principles from project context)
  - Governance (amendment procedure, versioning, compliance)
Removed sections: None
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section ready for principle gates
  ✅ spec-template.md - Scope/requirements align with specification-first principle
  ✅ tasks-template.md - Task categorization reflects layer separation and service composition
  ✅ phr-template.prompt.md - PHR requirement already embedded
Follow-up TODOs: None
-->

# Evolution of Todo Constitution

## Core Principles

### I. Specification-First Development (NON-NEGOTIABLE)

No implementation code may be generated unless an approved specification exists. All behavior must be traceable to a specification file inside `/specs-history`. Specifications are the single source of truth for feature behavior, requirements, and acceptance criteria. Implementation without an approved spec is a violation of this principle.

**Rationale**: Ensures deliberate design, prevents technical debt from un-planned features, and maintains traceability from business intent to code. This principle enables long-term system evolution by keeping all behavior documented and auditable.

### II. Layer Separation

Domain logic must be completely isolated from I/O, CLI, and infrastructure layers. The core domain must be deterministic, testable, and framework-free. Dependencies must always point inward (infrastructure depends on domain, never the reverse).

**Rationale**: Enables independent testing, technology substitution, and migration to distributed architectures without rewriting business logic. Isolated domain logic can run in any environment (CLI, API, serverless, Kubernetes) unchanged.

### III. Backward Compatibility

Every phase must preserve backward compatibility with previous phases. Phase I is the canonical business engine and all future phases must treat it as the foundation. Breaking changes require explicit architectural decision records and migration plans.

**Rationale**: Enables incremental delivery without disrupting existing functionality. Users can rely on system stability as it evolves from Phase I to more complex architectures.

### IV. Service-Oriented Architecture

All features must be implemented as composable services, not scripts. Services expose clear interfaces, maintain stateless operation where possible, and can be combined to create complex workflows. Scripts are prohibited except for build/deployment automation.

**Rationale**: Enables horizontal scaling, parallel execution, and future migration to microservices or serverless architectures. Composable services can be orchestrated by AI or Kubernetes in later phases.

### V. Explicit Data Models

Data models must be explicit, typed, and versionable. All domain entities must be defined with clear schemas, validation rules, and version identifiers. Implicit or dynamic data structures are prohibited in the domain layer.

**Rationale**: Enables schema evolution, data migration planning, and type-safe communication between services. Versionable models support gradual system evolution without breaking contracts.

### VI. Phase I Constraints

No persistence is allowed in Phase I beyond in-memory repositories. All data storage must use in-memory collections that simulate persistence behavior. File systems, databases, or external storage are explicitly prohibited in Phase I.

**Rationale**: Forces focus on pure domain logic before introducing infrastructure complexity. In-memory repositories provide the same interface as future persistent stores, enabling smooth transition without domain code changes.

### VII. Canonical Business Engine

All future phases must treat Phase I as the canonical business engine. Phase I contains the pure domain logic and business rules that never change across architecture evolution. Later phases only add infrastructure, distribution, or orchestration around this core.

**Rationale**: Enables risk-free architecture evolution. By treating Phase I as immutable, we can migrate from CLI to API to Kubernetes to AI-orchestrated without touching business logic.

### VIII. Evolutionary Architecture

The system must be designed so it can evolve into a distributed, event-driven, AI-orchestrated Kubernetes platform without refactoring the core domain. All Phase I design decisions must anticipate this evolutionary path. Domain code must be infrastructure-agnostic and ready for containerization, service mesh, and orchestration.

**Rationale**: Prevents architectural dead-ends that would require domain refactoring when scaling. Designing for evolution from day one avoids costly rewrites and supports the system's growth from simple CLI to complex distributed platform.

## Development Standards

### Authoritative Source Mandate

Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification through command output or API calls.

### PHR for Every User Input

Create a Prompt History Record (PHR) after every user interaction. PHRs preserve the complete conversation history including full user input, AI responses, outcomes, and reflections. This enables learning, traceability, and pattern recognition across the development lifecycle.

### Architectural Decision Records

When architecturally significant decisions are made (framework selection, data model design, API contracts, security approaches, deployment strategy), an ADR must be created. Significance is determined by three criteria: long-term impact, multiple viable alternatives, cross-cutting scope.

### Human as Tool Strategy

Invoke the user for input when encountering situations requiring human judgment: ambiguous requirements, unforeseen dependencies, architectural uncertainty, or completion checkpoints. Treat users as specialized tools for clarification and decision-making, not as obstacles.

### Smallest Viable Change

Prefer the smallest viable diff. Do not refactor unrelated code. Every change must be justified by a specification requirement or architectural need. Avoid premature optimization, feature creep, or "improvements" beyond what is explicitly requested.

## Governance

### Amendment Procedure

The constitution supersedes all other project practices. Amendments require:
1. Documented proposal with justification
2. Team review and approval
3. Migration plan for existing code and specs
4. Version increment according to semantic versioning

### Versioning Policy

- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review

All pull requests and reviews must verify compliance with constitution principles. Complexity violations must be documented with justification in the Complexity Tracking section of plan.md. Use CLAUDE.md for runtime development guidance. The constitution is the final authority on acceptable practices.

**Version**: 1.0.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-04
