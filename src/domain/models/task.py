"""
Task entity for Todo system.
Phase I: Core task model with frozen dataclass for immutability.
"""
from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration.

    Binary status for Phase I: PENDING or COMPLETED.
    No intermediate states (e.g., in_progress, blocked) in Phase I.
    """
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass(frozen=True)
class Task:
    """Task entity representing a unit of work.

    The Task is immutable after creation (frozen=True). To update
    a task, create a new Task instance with modified fields.

    This design ensures:
    - Deterministic behavior (FR-002, FR-011)
    - Clear state transitions (FR-006, FR-007)
    - Support for future distributed systems (no shared mutable state)

    Attributes:
        id: Unique task identifier (format: "task-{number}")
        description: Task description text (1-256 characters)
        status: Current task status (pending or completed)
    """
    id: str
    description: str
    status: TaskStatus

    def __post_init__(self):
        """Validate task fields after initialization.

        FR-010: Reject empty or whitespace-only descriptions.
        Assumption: Description max length is 256 characters.
        """
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        if len(self.description) > 256:
            raise ValueError("Task description cannot exceed 256 characters")
