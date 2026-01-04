"""
Abstract base class for task repository implementations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

# Import after models are created
# from src.domain.models import Task, TaskStatus


class TaskRepository(ABC):
    """Abstract repository interface for task persistence operations."""

    @abstractmethod
    def create(self, task: "Task") -> "Task":
        """Create a task in the repository.

        Args:
            task: Task entity to create (must have unique ID)

        Returns:
            Task: The created task

        Raises:
            DuplicateTaskError: If a task with the same ID already exists
        """
        pass

    @abstractmethod
    def get(self, task_id: str) -> Optional["Task"]:
        """Get a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        pass

    @abstractmethod
    def list(self) -> List["Task"]:
        """Get all tasks.

        Returns:
            List[Task]: List of all tasks in the repository
        """
        pass

    @abstractmethod
    def update(self, task: "Task") -> "Task":
        """Update a task in the repository.

        Args:
            task: Task entity with updated fields

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Delete a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            bool: True if task was deleted, False if not found
        """
        pass

    @abstractmethod
    def filter_by_status(self, status: "TaskStatus") -> List["Task"]:
        """Filter tasks by status.

        Args:
            status: Status to filter by (PENDING or COMPLETED)

        Returns:
            List[Task]: List of tasks with the specified status
        """
        pass
