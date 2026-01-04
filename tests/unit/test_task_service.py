"""
Unit tests for TaskService.
"""
import pytest

from src.domain.repositories.in_memory import InMemoryTaskRepository
from src.domain.services.task_service import TaskService
from src.lib.identifiers import IdentifierGenerator
from src.domain.models.task import TaskStatus
from src.domain.exceptions import TaskNotFoundError


class TestTaskService:
    """Unit tests for TaskService business logic."""

    def setup_method(self):
        """Initialize service for each test."""
        self.repo = InMemoryTaskRepository()
        self.id_gen = IdentifierGenerator()
        self.service = TaskService(self.repo, self.id_gen)

    # Create task tests
    def test_service_create_task(self):
        """Test creating a task through service."""
        task = self.service.create_task("Buy groceries")
        assert task.description == "Buy groceries"
        assert task.status == TaskStatus.PENDING
        assert task.id is not None

    # Update status tests
    def test_service_update_status(self):
        """Test updating task status."""
        task = self.service.create_task("Test task")
        assert task.status == TaskStatus.PENDING

        updated = self.service.update_status(task.id, TaskStatus.COMPLETED)
        assert updated.status == TaskStatus.COMPLETED

    def test_service_update_status_non_existent_raises(self):
        """Test updating non-existent task raises."""
        with pytest.raises(TaskNotFoundError):
            self.service.update_status("task-999999", TaskStatus.COMPLETED)

    # List tasks tests
    def test_service_list_tasks(self):
        """Test listing all tasks."""
        self.service.create_task("Task 1")
        self.service.create_task("Task 2")

        tasks = self.service.list_tasks()
        assert len(tasks) == 2

    def test_service_list_tasks_with_filter(self):
        """Test listing tasks with status filter."""
        self.service.create_task("Task 1")
        self.service.create_task("Task 2")
        task3 = self.service.create_task("Task 3")

        # Mark one as completed
        self.service.update_status(task3.id, TaskStatus.COMPLETED)

        # Filter by pending
        pending = self.service.list_tasks(TaskStatus.PENDING)
        assert len(pending) == 2
        assert all(t.status == TaskStatus.PENDING for t in pending)

        # Filter by completed
        completed = self.service.list_tasks(TaskStatus.COMPLETED)
        assert len(completed) == 1
        assert completed[0].status == TaskStatus.COMPLETED

    # Get task tests
    def test_service_get_task(self):
        """Test getting a task."""
        created = self.service.create_task("Test task")
        retrieved = self.service.get_task(created.id)

        assert retrieved.id == created.id
        assert retrieved.description == "Test task"

    def test_service_get_task_non_existent_raises(self):
        """Test getting non-existent task raises."""
        with pytest.raises(TaskNotFoundError):
            self.service.get_task("task-999999")

    # Delete task tests
    def test_service_delete_task(self):
        """Test deleting a task."""
        task = self.service.create_task("To delete")

        tasks_before = self.service.list_tasks()
        assert len(tasks_before) == 1

        self.service.delete_task(task.id)

        tasks_after = self.service.list_tasks()
        assert len(tasks_after) == 0

    def test_service_delete_task_non_existent_raises(self):
        """Test deleting non-existent task raises."""
        with pytest.raises(TaskNotFoundError):
            self.service.delete_task("task-999999")
