# Research: Evolution of Todo - Core Task Management

**Feature**: 001-todo-spec-system | **Date**: 2026-01-04 | **Spec**: [spec.md](./spec.md)

## Research Scope

Phase 0 research validates technical context decisions and ensures all unknowns are resolved before Phase 1 design. This research documents rationale for technology choices and best practices relevant to Phase I implementation.

## Technology Decisions

### Language Selection: Python 3.11

**Decision**: Use Python 3.11 for Phase I implementation

**Rationale**:
- Clear, readable syntax aligns with specification-first development philosophy
- Strong typing support via dataclasses and typing module enables explicit data models
- Native dataclass decorators provide clean entity definitions without boilerplate
- Standard library robust (collections, abc, dataclasses, typing)
- Cross-platform CLI support (built-in argparse/click)
- Industry-standard testing framework (pytest)
- Widely understood, facilitates team collaboration and code review
- Future-ready: can containerize, deploy to cloud, integrate with Kubernetes in later phases

**Alternatives Considered**:

| Alternative | Evaluation | Rejection Reason |
|------------|------------|------------------|
| Rust | Excellent performance, strong type system | Steeper learning curve, less readable for specification-traceable code |
| Go | Good performance, simple syntax | Less mature data modeling, verbose entity definitions |
| TypeScript | Strong typing, modern syntax | Requires build step, adds complexity for Phase I CLI |
| Java | Mature ecosystem, enterprise-grade | Verbose, less suitable for rapid prototyping |

### Testing Framework: pytest

**Decision**: Use pytest for all testing (unit, integration, contract)

**Rationale**:
- De facto standard for Python testing
- Powerful fixtures enable clean test setup/teardown
- Clear, readable assertion syntax
- Built-in discovery and test collection
- Supports parameterized tests for edge case coverage
- Easy integration with CI/CD pipelines for future phases
- Active community and extensive documentation

**Best Practices**:
- Unit tests: Isolate individual components (Task entity, repository, service)
- Integration tests: Verify service layer composition with repository
- Contract tests: Ensure TaskService behavior matches specification FRs
- Edge case tests: Cover empty descriptions, non-existent IDs, duplicate operations

### Repository Pattern: In-Memory Implementation

**Decision**: Implement abstract repository interface with in-memory concrete implementation

**Rationale**:
- Provides persistence abstraction (interface) while meeting Phase I constraints
- Enables smooth migration to file system/database in Phase II without domain code changes
- InMemoryRepository uses Python dict/list - simple, deterministic, testable
- Abstract base class enforces interface contract (create, get, list, update, delete, filter)

**Design Pattern**:
```python
# Abstract base (domain layer)
class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task: ...
    @abstractmethod
    def get(self, task_id: str) -> Optional[Task]: ...

# Concrete implementation (domain layer)
class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._counter: int = 0
```

**Alternatives Considered**:

| Alternative | Evaluation | Rejection Reason |
|------------|------------|------------------|
| Direct dict access | Simpler, no abstraction | Tight coupling, violates layer separation principle |
| Global singleton state | Easiest to implement | Violates service-oriented architecture, non-testable |

### ID Generation: Sequential Counter

**Decision**: Use sequential integer IDs for task identification

**Rationale**:
- Deterministic and predictable (aligns with constitution requirements)
- Simple to implement (counter + formatting)
- Easy to test (predictable sequence)
- Human-readable for CLI interaction
- Can migrate to UUID in Phase II if needed for distributed systems

**Implementation**:
```python
class IdentifierGenerator:
    def __init__(self):
        self._counter = 0

    def next_id(self) -> str:
        self._counter += 1
        return f"task-{self._counter:06d}"
```

**Alternatives Considered**:

| Alternative | Evaluation | Rejection Reason |
|------------|------------|------------------|
| UUID4 | Industry standard, collision-free | Non-deterministic, harder to test, overkill for Phase I |
| Timestamp-based | Simple | Collision risk, ordering issues |

## Architecture Decisions

### Service-Oriented Architecture

**Decision**: Implement TaskService as stateless business logic layer

**Rationale**:
- Services expose clear interfaces (methods) enabling composition
- Stateless operation enables horizontal scaling in future phases
- Separates business logic from data persistence
- Facilitates testing (inject mock repository)
- Supports evolution: service remains unchanged as infrastructure layers added

**Service Interface**:
```python
class TaskService:
    def __init__(self, repository: TaskRepository):
        self._repo = repository
        self._id_gen = IdentifierGenerator()

    # Stateless business methods
    def create_task(self, description: str) -> Task: ...
    def get_task(self, task_id: str) -> Task: ...
    def list_tasks(self, status_filter: Optional[str]) -> List[Task]: ...
    def update_status(self, task_id: str, status: str) -> Task: ...
    def delete_task(self, task_id: str) -> None: ...
```

### Layer Separation

**Decision**: Enforce strict layer separation with inward dependency flow

**Architecture Layers**:
1. **Domain Layer** (src/domain/): Pure business logic
   - Models: Task entity
   - Repositories: Abstract interface + in-memory implementation
   - Services: TaskService (business rules)

2. **Interface Layer** (src/interface/): I/O orchestration
   - CLI: User interaction, argument parsing, output formatting
   - Depends on domain layer (services)

3. **Utility Layer** (src/lib/): Cross-cutting utilities
   - Identifier generation

**Dependency Rule**: Interface → Domain (never reverse)

**Rationale**:
- Enables independent testing of domain logic
- Allows interface substitution (CLI → API → Event Bus) without domain changes
- Supports Phase II/III evolution by adding new interface layers
- Aligns with constitution principle II (Layer Separation)

## Evolution Readiness

### Phase I → Phase II Migration Path

**Phase I (Current)**:
- CLI interface
- In-memory repository
- Single-user, session-scoped

**Phase II (Future)**:
- REST API interface (add src/interface/api.py)
- File system repository (add src/domain/repositories/file.py)
- Multi-user support via separate in-memory instances

**Migration Approach**:
1. Add new interface layer (REST API) - no domain changes
2. Add new repository implementation (file-based) - swap with InMemoryRepository
3. Domain code remains unchanged (canonical business engine preserved)

### Phase II → Phase III Migration Path

**Phase III (Future)**:
- Kubernetes deployment
- Event-driven architecture
- AI orchestration
- Distributed task service

**Migration Approach**:
1. Containerize existing CLI and API interfaces
2. Add event bus interface (TaskEventPublisher service)
3. Deploy TaskService as microservice with existing interfaces
4. Domain code remains unchanged

**Key Insight**: By keeping domain code infrastructure-agnostic in Phase I, we enable future phases to add complexity (persistence, distribution, orchestration) without refactoring business logic.

## Constraints & Invariants

### Phase I Constraints (from Constitution)

1. **No file system/database persistence**: Use in-memory collections only
   - Enforced by not importing os/path modules in domain layer
   - InMemoryRepository uses dict/list internally

2. **Framework-free domain layer**: No external dependencies in src/domain/
   - Use Python standard library only (dataclass, abc, typing, collections)
   - CLI frameworks (click, typer) limited to interface layer

3. **Deterministic behavior**: No randomness, no global state
   - Use sequential ID generator
   - Testable, reproducible

### System Invariants

1. **Task ID uniqueness**: Guaranteed by repository implementation
2. **Task status binary**: Only "pending" or "completed"
3. **Single-user context**: No authentication/authorization in Phase I
4. **Session-scoped data**: All data lost on process termination

## Testing Strategy

### Test Categories

1. **Unit Tests** (tests/unit/):
   - `test_task.py`: Task entity validation, field constraints
   - `test_in_memory_repository.py`: Repository CRUD, uniqueness guarantees
   - `test_task_service.py`: Business logic, error handling

2. **Integration Tests** (tests/integration/):
   - `test_task_workflow.py`: End-to-end task lifecycle (create → update → delete)

3. **Contract Tests** (tests/contract/):
   - `test_task_service.py`: Verify all functional requirements (FR-001 to FR-014)

### Test Coverage Goals

- Domain layer: 100% (canonical business engine must be thoroughly tested)
- Interface layer: 80% (CLI edge cases less critical for future evolution)
- Overall: 90%+ (industry standard for production code)

### Performance Benchmarks

- Create task: <3s (per SC-001)
- List 100 tasks: <1s (per SC-002)
- Update status: <1s (per SC-003)
- Support 10,000 tasks in memory: no degradation (per SC-006)

## Best Practices

### Python 3.11 Specific

- Use `dataclass` for entity definitions (clean, type-safe)
- Use `typing` module for explicit type hints (Service, Optional, List)
- Use `abc.ABC` for abstract interfaces (enforce contracts)
- Use f-strings for string formatting (readable, performant)

### Clean Code Principles

- Single responsibility: Each class/module has one purpose
- Dependency injection: Pass dependencies to constructors (testable)
- Interface segregation: Small, focused interfaces (repository methods)
- DRY (Don't Repeat Yourself): Shared utilities (IdentifierGenerator)

### Repository Pattern Best Practices

- Abstract base class defines contract (ABC)
- Concrete implementation is swappable (InMemoryRepository → FileRepository)
- Repository encapsulates data access (no direct dict access in services)
- Repository methods return domain entities (not raw dicts)

## Research Conclusion

All technical context decisions validated. Phase I implementation ready to proceed with:

- Python 3.11 for clear, maintainable code
- pytest for comprehensive testing
- Repository pattern for abstraction and evolution readiness
- Service-oriented architecture for composability
- Layer separation for future interface substitution

No unknowns remain. Ready for Phase 1 (data-model.md, contracts/, quickstart.md).
