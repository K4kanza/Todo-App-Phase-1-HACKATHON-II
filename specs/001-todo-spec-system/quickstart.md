# Quick Start Guide: Evolution of Todo - Phase I

**Feature**: 001-todo-spec-system | **Date**: 2026-01-04
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Overview

This guide provides step-by-step instructions to get the Phase I Todo system up and running. Phase I is a CLI-based task management system with in-memory persistence.

## Prerequisites

- Python 3.11 or later
- Git (for version control)
- Terminal/Command Prompt

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd Todo-App-Phase-1-HACKATHON-II
```

### 2. Check Out Feature Branch

```bash
git checkout 001-todo-spec-system
```

### 3. Create Virtual Environment

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install pytest
```

Create `requirements.txt`:

```text
pytest>=7.4.0
```

### 5. Verify Installation

```bash
python --version  # Should be 3.11+
pytest --version  # Should show pytest 7.4.0+
```

## Project Structure

```
Todo-App-Phase-1-HACKATHON-II/
├── specs/
│   └── 001-todo-spec-system/
│       ├── spec.md           # Feature specification
│       ├── plan.md           # Implementation plan
│       ├── research.md       # Research findings
│       ├── data-model.md     # Data model definition
│       ├── quickstart.md     # This file
│       ├── contracts/
│       │   └── task-service.md  # Service contract
│       └── tasks.md          # Implementation tasks (TBD)
├── src/
│   ├── domain/
│   │   ├── models/
│   │   │   └── task.py               # Task entity
│   │   ├── repositories/
│   │   │   ├── base.py               # Repository interface
│   │   │   └── in_memory.py          # In-memory implementation
│   │   ├── services/
│   │   │   └── task_service.py       # Business logic
│   │   └── exceptions.py             # Custom exceptions
│   ├── interface/
│   │   └── cli.py                    # CLI interface
│   └── lib/
│       └── identifiers.py            # ID generator
├── tests/
│   ├── contract/
│   │   └── test_task_service.py      # Contract tests
│   ├── integration/
│   │   └── test_task_workflow.py     # E2E tests
│   └── unit/
│       ├── test_task.py              # Entity tests
│       ├── test_in_memory_repository.py
│       └── test_task_service.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Implementation Steps

### Phase 0: Setup (Already Complete)

- [x] Repository initialized
- [x] Feature branch created
- [x] Specification written
- [x] Plan and research documents created
- [x] Data model defined
- [x] Service contract specified

### Phase 1: Data Model Implementation

**Files to Create**:

1. `src/domain/models/task.py` - Task entity

```python
from dataclasses import dataclass
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

@dataclass(frozen=True)
class Task:
    id: str
    description: str
    status: TaskStatus

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        if len(self.description) > 256:
            raise ValueError("Task description cannot exceed 256 characters")
```

2. `src/domain/exceptions.py` - Custom exceptions

```python
class TaskNotFoundError(Exception):
    pass

class DuplicateTaskError(Exception):
    pass

class InvalidTaskError(Exception):
    pass
```

**Create directory**:
```bash
mkdir -p src/domain/models src/domain/repositories src/domain/services src/interface src/lib tests/contract tests/integration tests/unit
```

### Phase 2: Repository Implementation

**Files to Create**:

3. `src/domain/repositories/base.py` - Repository interface

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import Task, TaskStatus

class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task: ...

    @abstractmethod
    def get(self, task_id: str) -> Optional[Task]: ...

    @abstractmethod
    def list(self) -> List[Task]: ...

    @abstractmethod
    def update(self, task: Task) -> Task: ...

    @abstractmethod
    def delete(self, task_id: str) -> bool: ...

    @abstractmethod
    def filter_by_status(self, status: TaskStatus) -> List[Task]: ...
```

4. `src/lib/identifiers.py` - ID generator

```python
class IdentifierGenerator:
    def __init__(self):
        self._counter = 0

    def next_id(self) -> str:
        self._counter += 1
        return f"task-{self._counter:06d}"
```

5. `src/domain/repositories/in_memory.py` - In-memory repository

```python
from typing import Dict, List, Optional
from src.domain.repositories.base import TaskRepository
from src.domain.models import Task, TaskStatus
from src.domain.exceptions import DuplicateTaskError

class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def create(self, task: Task) -> Task:
        if task.id in self._tasks:
            raise DuplicateTaskError(f"Task with ID {task.id} already exists")
        self._tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def list(self) -> List[Task]:
        return list(self._tasks.values())

    def update(self, task: Task) -> Task:
        if task.id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task.id} not found")
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        return [t for t in self._tasks.values() if t.status == status]
```

### Phase 3: Service Implementation

6. `src/domain/services/task_service.py` - Business logic

```python
from typing import List, Optional
from src.domain.repositories.base import TaskRepository
from src.domain.models import Task, TaskStatus
from src.domain.exceptions import TaskNotFoundError
from src.lib.identifiers import IdentifierGenerator

class TaskService:
    def __init__(self, repository: TaskRepository, id_generator: IdentifierGenerator):
        self._repo = repository
        self._id_gen = id_generator

    def create_task(self, description: str) -> Task:
        task = Task(
            id=self._id_gen.next_id(),
            description=description,
            status=TaskStatus.PENDING
        )
        return self._repo.create(task)

    def get_task(self, task_id: str) -> Task:
        task = self._repo.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task

    def list_tasks(self, status_filter: Optional[TaskStatus] = None) -> List[Task]:
        if status_filter:
            return self._repo.filter_by_status(status_filter)
        return self._repo.list()

    def update_status(self, task_id: str, status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        updated_task = Task(id=task.id, description=task.description, status=status)
        return self._repo.update(updated_task)

    def delete_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        self._repo.delete(task_id)
```

### Phase 4: CLI Implementation

7. `src/interface/cli.py` - Command-line interface

```python
import sys
import argparse
from src.domain.repositories.in_memory import InMemoryTaskRepository
from src.domain.services.task_service import TaskService
from src.lib.identifiers import IdentifierGenerator
from src.domain.models import TaskStatus

def main():
    parser = argparse.ArgumentParser(description="Todo Task Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # create command
    create_parser = subparsers.add_parser('create', help='Create a new task')
    create_parser.add_argument('description', help='Task description')

    # list command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--status', choices=['pending', 'completed'],
                            help='Filter by status')

    # update command
    update_parser = subparsers.add_parser('update', help='Update task status')
    update_parser.add_argument('id', help='Task ID')
    update_parser.add_argument('status', choices=['pending', 'completed'],
                              help='New status')

    # delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', help='Task ID')

    args = parser.parse_args()

    # Initialize service
    repo = InMemoryTaskRepository()
    id_gen = IdentifierGenerator()
    service = TaskService(repo, id_gen)

    try:
        if args.command == 'create':
            task = service.create_task(args.description)
            print(f"Created: [{task.id}] {task.description} ({task.status.value})")

        elif args.command == 'list':
            status = TaskStatus(args.status) if args.status else None
            tasks = service.list_tasks(status)
            for task in tasks:
                print(f"[{task.id}] {task.description} ({task.status.value})")

        elif args.command == 'update':
            status = TaskStatus(args.status)
            task = service.update_status(args.id, status)
            print(f"Updated: [{task.id}] {task.description} ({task.status.value})")

        elif args.command == 'delete':
            service.delete_task(args.id)
            print(f"Deleted: {args.id}")

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

## Usage Examples

### Create a Task

```bash
python -m src.interface.cli create "Buy groceries"
# Output: Created: [task-000001] Buy groceries (pending)
```

### List All Tasks

```bash
python -m src.interface.cli list
# Output:
# [task-000001] Buy groceries (pending)
# [task-000002] Finish report (completed)
```

### List Pending Tasks Only

```bash
python -m src.interface.cli list --status pending
# Output:
# [task-000001] Buy groceries (pending)
```

### Update Task Status

```bash
python -m src.interface.cli update task-000001 completed
# Output: Updated: [task-000001] Buy groceries (completed)
```

### Delete a Task

```bash
python -m src.interface.cli delete task-000001
# Output: Deleted: task-000001
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests only
pytest tests/contract/       # Contract tests only
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

View coverage report: `htmlcov/index.html`

### Expected Test Coverage

- Domain layer: 100%
- Interface layer: 80%
- Overall: 90%+

## Verification Checklist

### Functional Requirements

- [ ] FR-001: Can create tasks with description
- [ ] FR-002: Tasks have unique IDs
- [ ] FR-003: New tasks start as pending
- [ ] FR-004: Can list all tasks
- [ ] FR-005: Can get specific task by ID
- [ ] FR-006: Can update status to completed
- [ ] FR-007: Can update status back to pending
- [ ] FR-008: Can delete tasks
- [ ] FR-009: Can filter tasks by status
- [ ] FR-010: Empty descriptions rejected
- [ ] FR-011: Duplicate IDs rejected
- [ ] FR-012: Non-existent tasks raise errors
- [ ] FR-013: Data persists in memory during session
- [ ] FR-014: Data lost on termination (Phase I)

### Success Criteria

- [ ] SC-001: Create task in under 3 seconds
- [ ] SC-002: List 100 tasks in under 1 second
- [ ] SC-003: Update status in under 1 second
- [ ] SC-004: 100% success rate with valid input
- [ ] SC-005: 95% first-time user success rate (manual verification)
- [ ] SC-006: Supports 10,000 tasks without degradation

### Constitution Compliance

- [ ] I. Specification-First Development: All code traces to spec
- [ ] II. Layer Separation: Domain isolated from CLI
- [ ] III. Backward Compatibility: N/A (Phase I)
- [ ] IV. Service-Oriented Architecture: Stateless services
- [ ] V. Explicit Data Models: Typed entities
- [ ] VI. Phase I Constraints: In-memory only, no file system
- [ ] VII. Canonical Business Engine: Domain is pure
- [ ] VIII. Evolutionary Architecture: Infrastructure-agnostic domain

## Troubleshooting

### Import Errors

If you get "ModuleNotFoundError" when running tests or CLI:

```bash
# Set PYTHONPATH to include src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%CD%          # Windows

# Or install in development mode
pip install -e .
```

### Test Failures

- Ensure pytest is installed: `pip install pytest`
- Check Python version: `python --version` (must be 3.11+)
- Verify all files are in correct directories

### Data Not Persisting

This is expected behavior for Phase I. All task data is stored in memory and will be lost when the application terminates. Persistence will be added in Phase II.

## Next Steps

After Phase I implementation is complete:

1. Run `/sp.tasks` to generate implementation tasks
2. Implement all tasks in priority order
3. Run contract tests to verify specification compliance
4. Create Phase II plan for adding persistence and API interface

## Resources

- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Research Findings](./research.md)
- [Data Model](./data-model.md)
- [Service Contract](./contracts/task-service.md)
- [Project Constitution](../../.specify/memory/constitution.md)

---

*Quick Start Guide complete. Ready for Phase II planning or task generation.*
