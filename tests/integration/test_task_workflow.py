"""
Integration tests for end-to-end workflows.
Tests verify user stories work end-to-end.
"""
import pytest

from src.domain.repositories.in_memory import InMemoryTaskRepository
from src.domain.services.task_service import TaskService
from src.lib.identifiers import IdentifierGenerator
from src.domain.models.task import TaskStatus


class TestTaskWorkflowIntegration:
    """Integration tests for complete task workflows."""

    def setup_method(self):
        """Initialize service for each test."""
        self.repo = InMemoryTaskRepository()
        self.id_gen = IdentifierGenerator()
        self.service = TaskService(self.repo, self.id_gen)

    # User Story 1: Create and List Tasks
    def test_create_and_list_workflow(self):
        """Test creating tasks and listing them end-to-end (US1)."""
        # Create multiple tasks
        t1 = self.service.create_task("Buy groceries")
        t2 = self.service.create_task("Finish report")
        t3 = self.service.create_task("Call doctor")

        # List all tasks
        tasks = self.service.list_tasks()

        assert len(tasks) == 3
        assert t1.id in [t.id for t in tasks]
        assert t2.id in [t.id for t in tasks]
        assert t3.id in [t.id for t in tasks]

        # Verify all are pending
        assert all(t.status == TaskStatus.PENDING for t in tasks)

    # User Story 2: Update Task Status
    def test_update_status_workflow(self):
        """Test updating task status end-to-end (US2)."""
        # Create task
        task = self.service.create_task("Test task")
        assert task.status == TaskStatus.PENDING

        # Update to completed
        completed = self.service.update_status(task.id, TaskStatus.COMPLETED)
        assert completed.status == TaskStatus.COMPLETED

        # Update back to pending
        pending = self.service.update_status(task.id, TaskStatus.PENDING)
        assert pending.status == TaskStatus.PENDING

    # User Story 3: Delete Tasks
    def test_delete_workflow(self):
        """Test deleting tasks end-to-end (US3)."""
        # Create multiple tasks
        t1 = self.service.create_task("Task 1")
        t2 = self.service.create_task("Task 2")
        t3 = self.service.create_task("Task 3")

        # Delete one
        self.service.delete_task(t2.id)

        # Verify it's gone
        tasks = self.service.list_tasks()
        assert len(tasks) == 2
        assert t1.id in [t.id for t in tasks]
        assert t3.id in [t.id for t in tasks]
        assert t2.id not in [t.id for t in tasks]

    # User Story 4: Filter Tasks by Status
    def test_filter_workflow(self):
        """Test filtering tasks by status end-to-end (US4)."""
        # Create tasks with mixed statuses
        t1 = self.service.create_task("Task 1")
        t2 = self.service.create_task("Task 2")
        t3 = self.service.create_task("Task 3")

        # Mark one as completed
        self.service.update_status(t2.id, TaskStatus.COMPLETED)

        # Filter by pending
        pending = self.service.list_tasks(TaskStatus.PENDING)
        assert len(pending) == 2
        assert all(t.status == TaskStatus.PENDING for t in pending)

        # Filter by completed
        completed = self.service.list_tasks(TaskStatus.COMPLETED)
        assert len(completed) == 1
        assert all(t.status == TaskStatus.COMPLETED for t in completed)

    # Performance test (SC-006)
    def test_performance_10k_tasks(self):
        """Test system handles 10,000 tasks without degradation (SC-006)."""
        import time

        # Create 10,000 tasks
        start = time.time()
        for i in range(10000):
            self.service.create_task(f"Task {i}")
        create_time = time.time() - start

        # List all tasks
        start = time.time()
        tasks = self.service.list_tasks()
        list_time = time.time() - start

        assert len(tasks) == 10000
        assert create_time < 10.0  # Should be much faster
        assert list_time < 1.0  # SC-002: <1s for 100 tasks, should scale

    # Edge case: Empty list
    def test_empty_list_workflow(self):
        """Test operations on empty task list."""
        tasks = self.service.list_tasks()
        assert tasks == []

        # Filter empty list
        pending = self.service.list_tasks(TaskStatus.PENDING)
        assert pending == []

        completed = self.service.list_tasks(TaskStatus.COMPLETED)
        assert completed == []
