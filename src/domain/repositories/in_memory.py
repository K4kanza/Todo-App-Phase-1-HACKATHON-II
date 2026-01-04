"""
In-memory implementation of task repository.
Phase I constraint: No file system or database persistence.
"""
from typing import Dict, List, Optional

from src.domain.repositories.base import TaskRepository
# Import after models are created
# from src.domain.models import Task, TaskStatus
from src.domain.exceptions import DuplicateTaskError


class InMemoryTaskRepository(TaskRepository):
    """In-memory repository for task storage using Python dict.

    Phase I constraint: All data is lost when application terminates.
    This is by design - Phase I establishes canonical business engine
    without infrastructure complexity. Persistence will be added in Phase II.
    """

    def __init__(self):
        """Initialize empty task storage."""
        self._tasks: Dict[str, "Task"] = {}

    def create(self, task: "Task") -> "Task":
        """Create a task in repository.

        Args:
            task: Task entity to create (must have unique ID)

        Returns:
            Task: The created task

        Raises:
            DuplicateTaskError: If a task with the same ID already exists
        """
        if task.id in self._tasks:
            raise DuplicateTaskError(f"Task with ID {task.id} already exists")
        self._tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Optional["Task"]:
        """Get a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def list(self) -> List["Task"]:
        """Get all tasks.

        Returns:
            List[Task]: List of all tasks in the repository
        """
        return list(self._tasks.values())

    def update(self, task: "Task") -> "Task":
        """Update a task in repository.

        Args:
            task: Task entity with updated fields

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        from src.domain.exceptions import TaskNotFoundError

        if task.id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task.id} not found")
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: str) -> bool:
        """Delete a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            bool: True if task was deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def filter_by_status(self, status: "TaskStatus") -> List["Task"]:
        """Filter tasks by status.

        Args:
            status: Status to filter by (PENDING or COMPLETED)

        Returns:
            List[Task]: List of tasks with the specified status
        """
        return [t for t in self._tasks.values() if t.status == status]
