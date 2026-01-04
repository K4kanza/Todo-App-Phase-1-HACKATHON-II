"""
Contract tests for TaskService behavior.
These tests verify all functional requirements (FR-001 to FR-014).
"""
import pytest

from src.domain.repositories.in_memory import InMemoryTaskRepository
from src.domain.services.task_service import TaskService
from src.lib.identifiers import IdentifierGenerator
from src.domain.models.task import TaskStatus
from src.domain.exceptions import TaskNotFoundError, DuplicateTaskError


class TestTaskServiceContract:
    """Contract tests for TaskService - all FRs must pass."""

    def setup_method(self):
        """Initialize service with fresh repository for each test."""
        self.repo = InMemoryTaskRepository()
        self.id_gen = IdentifierGenerator()
        self.service = TaskService(self.repo, self.id_gen)

    # FR-001: System MUST allow users to create tasks with text description
    def test_create_task_accepts_description(self):
        """FR-001: Create task with valid description."""
        task = self.service.create_task("Buy groceries")
        assert task.description == "Buy groceries"
        assert task.id is not None

    # FR-002: System MUST assign unique identifier to each task
    def test_create_task_generates_unique_id(self):
        """FR-002: Unique ID generated for each task."""
        task1 = self.service.create_task("Task 1")
        task2 = self.service.create_task("Task 2")
        assert task1.id != task2.id
        assert task1.id.startswith("task-")
        assert task2.id.startswith("task-")

    # FR-003: System MUST initialize all new tasks with "pending" status
    def test_create_task_initializes_pending_status(self):
        """FR-003: New tasks initialize as PENDING."""
        task = self.service.create_task("New task")
        assert task.status == TaskStatus.PENDING

    # FR-004: System MUST allow users to retrieve complete list of all tasks
    def test_list_tasks_returns_all_tasks(self):
        """FR-004: List all tasks returns all tasks."""
        self.service.create_task("Task 1")
        self.service.create_task("Task 2")
        self.service.create_task("Task 3")
        tasks = self.service.list_tasks()
        assert len(tasks) == 3

    # FR-005: System MUST allow users to retrieve specific task by ID
    def test_get_task_retrieves_by_id(self):
        """FR-005: Get task by ID."""
        created = self.service.create_task("Specific task")
        retrieved = self.service.get_task(created.id)
        assert retrieved.id == created.id
        assert retrieved.description == "Specific task"

    # FR-006: System MUST allow users to update task status from pending to completed
    def test_update_status_from_pending_to_completed(self):
        """FR-006: Update status from PENDING to COMPLETED."""
        task = self.service.create_task("Test task")
        assert task.status == TaskStatus.PENDING

        updated = self.service.update_status(task.id, TaskStatus.COMPLETED)
        assert updated.status == TaskStatus.COMPLETED

    # FR-007: System MUST allow users to update task status from completed to pending
    def test_update_status_from_completed_to_pending(self):
        """FR-007: Update status from COMPLETED to PENDING."""
        task = self.service.create_task("Test task")
        task = self.service.update_status(task.id, TaskStatus.COMPLETED)

        updated = self.service.update_status(task.id, TaskStatus.PENDING)
        assert updated.status == TaskStatus.PENDING

    # FR-008: System MUST allow users to delete tasks by ID
    def test_delete_task_removes_task(self):
        """FR-008: Delete task by ID."""
        task = self.service.create_task("To delete")
        tasks_before = self.service.list_tasks()

        self.service.delete_task(task.id)
        tasks_after = self.service.list_tasks()

        assert len(tasks_before) == 1
        assert len(tasks_after) == 0

    # FR-009: System MUST allow users to filter tasks by status
    def test_list_tasks_filters_by_status(self):
        """FR-009: Filter tasks by status."""
        self.service.create_task("Task 1")
        self.service.create_task("Task 2")
        self.service.create_task("Task 3")

        # Mark one as completed
        t1 = self.service.list_tasks()[0]
        self.service.update_status(t1.id, TaskStatus.COMPLETED)

        # Filter by pending
        pending = self.service.list_tasks(TaskStatus.PENDING)
        assert len(pending) == 2
        assert all(t.status == TaskStatus.PENDING for t in pending)

        # Filter by completed
        completed = self.service.list_tasks(TaskStatus.COMPLETED)
        assert len(completed) == 1
        assert all(t.status == TaskStatus.COMPLETED for t in completed)

    # FR-010: System MUST reject task creation with empty descriptions
    def test_create_task_rejects_empty_description(self):
        """FR-010: Reject empty description."""
        with pytest.raises(ValueError, match="cannot be empty"):
            self.service.create_task("")

        with pytest.raises(ValueError, match="cannot be empty"):
            self.service.create_task("   ")

    # FR-011: System MUST reject duplicate task IDs
    def test_create_task_rejects_duplicate_id(self):
        """FR-011: Duplicate IDs rejected."""
        # This is enforced by repository
        task = self.service.create_task("Task 1")
        with pytest.raises(DuplicateTaskError, match="already exists"):
            # Try to create another task with same ID (not directly possible via service)
            self.repo.create(task)  # Direct repository access for test

    # FR-012: System MUST return error for non-existent task
    def test_operations_reject_non_existent_task(self):
        """FR-012: Operations reject non-existent task."""
        non_existent_id = "task-999999"

        with pytest.raises(TaskNotFoundError, match="not found"):
            self.service.get_task(non_existent_id)

        with pytest.raises(TaskNotFoundError, match="not found"):
            self.service.update_status(non_existent_id, TaskStatus.COMPLETED)

        with pytest.raises(TaskNotFoundError, match="not found"):
            self.service.delete_task(non_existent_id)

    # FR-013: System MUST persist task data in memory
    def test_data_persists_in_memory_during_session(self):
        """FR-013: Data persists in memory during session."""
        task1 = self.service.create_task("Task 1")
        task2 = self.service.create_task("Task 2")

        # Data should still be accessible
        tasks = self.service.list_tasks()
        assert len(tasks) == 2
        assert any(t.id == task1.id for t in tasks)
        assert any(t.id == task2.id for t in tasks)
