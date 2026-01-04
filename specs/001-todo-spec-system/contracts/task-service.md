# Task Service Contract

**Feature**: 001-todo-spec-system | **Date**: 2026-01-04 | **Version**: 1.0.0
**Spec**: [spec.md](../spec.md) | **Data Model**: [data-model.md](../data-model.md)

## Overview

The TaskService contract defines the interface for task management operations. This contract is the canonical definition of business behavior and must be implemented exactly as specified.

## Service Definition

**Interface**: `TaskService` (abstract base class)

**Location**: `src/domain/services/task_service.py`

**Purpose**: Stateless business logic for task management operations. Provides task CRUD, status updates, and filtering.

## Public Interface

### Constructor

```python
class TaskService:
    """Task management service.

    The service is stateless - all state is managed by the injected
    repository and identifier generator. This enables horizontal scaling
    and testability.

    Args:
        repository: TaskRepository implementation for data persistence
        id_generator: IdentifierGenerator for unique task IDs
    """

    def __init__(
        self,
        repository: TaskRepository,
        id_generator: IdentifierGenerator
    ):
        self._repo = repository
        self._id_gen = id_generator
```

**Dependencies**:
- `TaskRepository` (see [Repository Contract](#repository-contract))
- `IdentifierGenerator` (see [Identifier Generator Contract](#identifier-generator-contract))

### Methods

#### create_task

**Purpose**: Create a new task with auto-generated ID (FR-001, FR-002, FR-003)

**Signature**:
```python
def create_task(self, description: str) -> Task:
    """Create a new task.

    Generates a unique task ID, initializes status as PENDING,
    and persists the task via repository.

    Args:
        description: Task description text (1-256 characters, non-empty)

    Returns:
        Task: Newly created task with ID, description, and status

    Raises:
        ValueError: If description is empty or exceeds 256 characters

    Examples:
        >>> service.create_task("Buy groceries")
        Task(id='task-000001', description='Buy groceries', status=TaskStatus.PENDING)
    """
```

**Functional Requirements**:
- FR-001: Allow users to create tasks with text description
- FR-002: Assign unique identifier to each task
- FR-003: Initialize all new tasks with "pending" status

#### get_task

**Purpose**: Retrieve a specific task by its unique identifier (FR-005)

**Signature**:
```python
def get_task(self, task_id: str) -> Task:
    """Get a task by its ID.

    Args:
        task_id: Unique task identifier (format: "task-{number}")

    Returns:
        Task: The task with the specified ID

    Raises:
        TaskNotFoundError: If no task exists with the given ID

    Examples:
        >>> service.get_task("task-000001")
        Task(id='task-000001', description='Buy groceries', status=TaskStatus.PENDING)
    """
```

**Functional Requirements**:
- FR-005: Allow users to retrieve a specific task by unique identifier

#### list_tasks

**Purpose**: Retrieve all tasks or filter by status (FR-004, FR-009)

**Signature**:
```python
def list_tasks(self, status_filter: Optional[TaskStatus] = None) -> List[Task]:
    """List tasks, optionally filtered by status.

    Args:
        status_filter: Optional status filter (PENDING or COMPLETED)
                     If None, returns all tasks

    Returns:
        List[Task]: List of tasks matching the filter criteria

    Examples:
        >>> service.list_tasks()
        [Task('task-000001', 'Buy groceries', PENDING), Task('task-000002', 'Finish report', COMPLETED)]

        >>> service.list_tasks(status_filter=TaskStatus.PENDING)
        [Task('task-000001', 'Buy groceries', PENDING)]
    """
```

**Functional Requirements**:
- FR-004: Allow users to retrieve complete list of all tasks
- FR-009: Allow users to filter tasks by status

#### update_status

**Purpose**: Update task status between pending and completed (FR-006, FR-007)

**Signature**:
```python
def update_status(self, task_id: str, status: TaskStatus) -> Task:
    """Update a task's status.

    Updates the specified task's status and persists the change.
    Creates a new Task instance with the updated status.

    Args:
        task_id: Unique task identifier
        status: New status (PENDING or COMPLETED)

    Returns:
        Task: The updated task with new status

    Raises:
        TaskNotFoundError: If no task exists with the given ID

    Examples:
        >>> service.update_status("task-000001", TaskStatus.COMPLETED)
        Task(id='task-000001', description='Buy groceries', status=TaskStatus.COMPLETED)
    """
```

**Functional Requirements**:
- FR-006: Allow users to update task status from "pending" to "completed"
- FR-007: Allow users to update task status from "completed" to "pending"

#### delete_task

**Purpose**: Delete a task by its unique identifier (FR-008)

**Signature**:
```python
def delete_task(self, task_id: str) -> None:
    """Delete a task by its ID.

    Args:
        task_id: Unique task identifier

    Raises:
        TaskNotFoundError: If no task exists with the given ID

    Examples:
        >>> service.delete_task("task-000001")
        # Task is removed from repository
    """
```

**Functional Requirements**:
- FR-008: Allow users to delete tasks by unique identifier

## Repository Contract

**Interface**: `TaskRepository` (abstract base class)

**Location**: `src/domain/repositories/base.py`

**Purpose**: Abstraction for task data persistence. Enables swapping storage implementations.

### Methods

#### create

```python
@abstractmethod
def create(self, task: Task) -> Task:
    """Create a task in the repository.

    Args:
        task: Task entity to create (must have unique ID)

    Returns:
        Task: The created task

    Raises:
        DuplicateTaskError: If a task with the same ID already exists
    """
```

#### get

```python
@abstractmethod
def get(self, task_id: str) -> Optional[Task]:
    """Get a task by ID.

    Args:
        task_id: Unique task identifier

    Returns:
        Optional[Task]: The task if found, None otherwise
    """
```

#### list

```python
@abstractmethod
def list(self) -> List[Task]:
    """Get all tasks.

    Returns:
        List[Task]: List of all tasks in the repository
    """
```

#### update

```python
@abstractmethod
def update(self, task: Task) -> Task:
    """Update a task in the repository.

    Args:
        task: Task entity with updated fields

    Returns:
        Task: The updated task

    Raises:
        TaskNotFoundError: If no task exists with the given ID
    """
```

#### delete

```python
@abstractmethod
def delete(self, task_id: str) -> bool:
    """Delete a task by ID.

    Args:
        task_id: Unique task identifier

    Returns:
        bool: True if task was deleted, False if not found
    """
```

#### filter_by_status

```python
@abstractmethod
def filter_by_status(self, status: TaskStatus) -> List[Task]:
    """Filter tasks by status.

    Args:
        status: Status to filter by (PENDING or COMPLETED)

    Returns:
        List[Task]: List of tasks with the specified status
    """
```

## Identifier Generator Contract

**Interface**: `IdentifierGenerator`

**Location**: `src/lib/identifiers.py`

**Purpose**: Generate unique, sequential task identifiers.

### Method

```python
class IdentifierGenerator:
    """Generate sequential task IDs.

    IDs are deterministic and follow the format "task-{number}"
    where number is zero-padded to 6 digits (e.g., "task-000001").

    Examples:
        >>> gen = IdentifierGenerator()
        >>> gen.next_id()
        'task-000001'
        >>> gen.next_id()
        'task-000002'
    """

    def __init__(self):
        """Initialize counter at 0"""
        self._counter = 0

    def next_id(self) -> str:
        """Generate the next unique ID.

        Returns:
            str: Sequential ID in format "task-{number}"
        """
        self._counter += 1
        return f"task-{self._counter:06d}"
```

## Error Handling

### Custom Exceptions

**Location**: `src/domain/exceptions.py`

```python
class TaskNotFoundError(Exception):
    """Raised when a task with the specified ID does not exist."""
    pass

class DuplicateTaskError(Exception):
    """Raised when attempting to create a task with a duplicate ID."""
    pass

class InvalidTaskError(Exception):
    """Raised when task validation fails (e.g., empty description)."""
    pass
```

### Error Response Mapping

| Service Method | Error Condition | Exception | HTTP Equivalent (Phase II) |
|---------------|----------------|-----------|---------------------------|
| `create_task` | Empty description | `ValueError` | 400 Bad Request |
| `create_task` | Duplicate ID | `DuplicateTaskError` | 409 Conflict |
| `get_task` | Task not found | `TaskNotFoundError` | 404 Not Found |
| `update_status` | Task not found | `TaskNotFoundError` | 404 Not Found |
| `delete_task` | Task not found | `TaskNotFoundError` | 404 Not Found |

## Test Contracts

### Contract Tests (tests/contract/)

Contract tests verify that the TaskService implementation matches this specification exactly.

**Test File**: `tests/contract/test_task_service.py`

**Test Cases**:
1. `test_create_task_generates_unique_id()`: Verify FR-002
2. `test_create_task_initializes_pending_status()`: Verify FR-003
3. `test_create_task_rejects_empty_description()`: Verify FR-010
4. `test_list_tasks_returns_all_tasks()`: Verify FR-004
5. `test_list_tasks_filters_by_status()`: Verify FR-009
6. `test_update_status_from_pending_to_completed()`: Verify FR-006
7. `test_update_status_from_completed_to_pending()`: Verify FR-007
8. `test_delete_task_removes_task()`: Verify FR-008
9. `test_operations_reject_non_existent_task()`: Verify FR-012

## Performance Contract

### Response Time Requirements

| Operation | Target | Maximum |
|-----------|---------|----------|
| `create_task` | <1s | 3s (SC-001) |
| `list_tasks` (100 tasks) | <0.5s | 1s (SC-002) |
| `update_status` | <0.5s | 1s (SC-003) |

### Scalability Requirements

- Support 10,000 tasks in memory without performance degradation (SC-006)
- Memory usage: <100MB for 10,000 tasks (estimated)

## Thread Safety

**Phase I Assumption**: Single-threaded execution (CLI interface).

**Phase II Note**: For multi-threaded or distributed systems, implement:
- Locking in repository methods
- Atomic operations for create/update/delete
- Consider thread-safe counter for IdentifierGenerator

## Versioning

**Current Version**: 1.0.0

**Contract Stability**: This contract is the canonical definition of TaskService behavior. Any changes require:
1. ADR documenting the change
2. Version bump (semantic versioning)
3. Migration plan if breaking changes
4. Update to contract tests

## Implementation Checklist

- [ ] TaskService class with all public methods defined
- [ ] TaskRepository abstract base class with all methods defined
- [ ] IdentifierGenerator class with next_id() method
- [ ] Custom exceptions defined (TaskNotFoundError, DuplicateTaskError, InvalidTaskError)
- [ ] All methods include type hints
- [ ] All methods include docstrings
- [ ] Contract tests pass for all functional requirements
- [ ] Performance benchmarks meet SC-001, SC-002, SC-003, SC-006

---

*Contract ready for implementation. See [quickstart.md](../quickstart.md) for setup and usage guide.*
