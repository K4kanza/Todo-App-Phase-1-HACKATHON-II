"""
Task service for business logic orchestration.
Phase I: Stateless service layer - enables future horizontal scaling.
"""
from typing import List, Optional

from src.domain.repositories.base import TaskRepository
from src.domain.models.task import Task, TaskStatus
from src.lib.identifiers import IdentifierGenerator
from src.domain.exceptions import TaskNotFoundError


class TaskService:
    """Task management service.

    The service is stateless - all state is managed by the injected
    repository and identifier generator. This enables horizontal scaling
    and testability. Design supports evolution to microservices in later phases.

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

    def create_task(self, description: str) -> Task:
        """Create a new task.

        Generates a unique task ID, initializes status as PENDING,
        and persists task via repository.

        FR-001: Allow users to create tasks with text description
        FR-002: Assign unique identifier to each task
        FR-003: Initialize all new tasks with "pending" status

        Args:
            description: Task description text (1-256 characters, non-empty)

        Returns:
            Task: Newly created task with ID, description, and status

        Raises:
            ValueError: If description is empty or exceeds 256 characters
        """
        task = Task(
            id=self._id_gen.next_id(),
            description=description,
            status=TaskStatus.PENDING
        )
        return self._repo.create(task)

    def get_task(self, task_id: str) -> Task:
        """Get a task by its ID.

        FR-005: Allow users to retrieve a specific task by unique identifier

        Args:
            task_id: Unique task identifier (format: "task-{number}")

        Returns:
            Task: The task with the specified ID

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        task = self._repo.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task

    def list_tasks(self, status_filter: Optional[TaskStatus] = None) -> List[Task]:
        """List tasks, optionally filtered by status.

        FR-004: Allow users to retrieve the complete list of all tasks
        FR-009: Allow users to filter tasks by status (pending or completed)

        Args:
            status_filter: Optional status filter (PENDING or COMPLETED)
                         If None, returns all tasks

        Returns:
            List[Task]: List of tasks matching the filter criteria
        """
        if status_filter:
            return self._repo.filter_by_status(status_filter)
        return self._repo.list()

    def update_status(self, task_id: str, status: TaskStatus) -> Task:
        """Update a task's status.

        Creates a new Task instance with updated status and persists
        the change. This functional approach supports future distributed systems.

        FR-006: Allow users to update task status from "pending" to "completed"
        FR-007: Allow users to update task status from "completed" to "pending"
        FR-012: Return appropriate error when attempting to update non-existent task

        Args:
            task_id: Unique task identifier
            status: New status (PENDING or COMPLETED)

        Returns:
            Task: The updated task with new status

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        task = self.get_task(task_id)
        # Create new Task instance with updated status (immutable design)
        updated_task = Task(id=task.id, description=task.description, status=status)
        return self._repo.update(updated_task)

    def delete_task(self, task_id: str) -> None:
        """Delete a task by its ID.

        FR-008: Allow users to delete tasks by unique identifier
        FR-012: Return appropriate error when attempting to delete non-existent task

        Args:
            task_id: Unique task identifier

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        task = self.get_task(task_id)
        self._repo.delete(task_id)
