"""
Unit tests for InMemoryTaskRepository implementation.
"""
import pytest

from src.domain.repositories.in_memory import InMemoryTaskRepository
from src.domain.models.task import Task, TaskStatus
from src.domain.exceptions import DuplicateTaskError


class TestInMemoryTaskRepository:
    """Unit tests for InMemoryTaskRepository."""

    def setup_method(self):
        """Initialize fresh repository for each test."""
        self.repo = InMemoryTaskRepository()

    # Test create method
    def test_repository_create_task(self):
        """Test creating a task."""
        task = Task(id="task-000001", description="Test task", status=TaskStatus.PENDING)
        created = self.repo.create(task)
        assert created.id == "task-000001"
        assert created.description == "Test task"

    def test_repository_create_duplicate_id_raises(self):
        """Test creating duplicate ID raises DuplicateTaskError."""
        task = Task(id="task-000001", description="Task 1", status=TaskStatus.PENDING)
        self.repo.create(task)

        duplicate = Task(id="task-000001", description="Task 2", status=TaskStatus.PENDING)
        with pytest.raises(DuplicateTaskError, match="already exists"):
            self.repo.create(duplicate)

    # Test get method
    def test_repository_get_existing_task(self):
        """Test getting an existing task."""
        task = Task(id="task-000001", description="Test task", status=TaskStatus.PENDING)
        self.repo.create(task)

        retrieved = self.repo.get("task-000001")
        assert retrieved is not None
        assert retrieved.id == "task-000001"

    def test_repository_get_non_existent_task_returns_none(self):
        """Test getting non-existent task returns None."""
        retrieved = self.repo.get("task-999999")
        assert retrieved is None

    # Test list method
    def test_repository_list_empty(self):
        """Test listing empty repository."""
        tasks = self.repo.list()
        assert tasks == []

    def test_repository_list_returns_all_tasks(self):
        """Test listing returns all tasks."""
        task1 = Task(id="task-000001", description="Task 1", status=TaskStatus.PENDING)
        task2 = Task(id="task-000002", description="Task 2", status=TaskStatus.COMPLETED)
        self.repo.create(task1)
        self.repo.create(task2)

        tasks = self.repo.list()
        assert len(tasks) == 2

    # Test update method
    def test_repository_update_task(self):
        """Test updating a task."""
        task = Task(id="task-000001", description="Original", status=TaskStatus.PENDING)
        self.repo.create(task)

        updated = Task(id="task-000001", description="Updated", status=TaskStatus.COMPLETED)
        result = self.repo.update(updated)

        assert result.description == "Updated"
        assert result.status == TaskStatus.COMPLETED

    def test_repository_update_non_existent_raises(self):
        """Test updating non-existent task raises TaskNotFoundError."""
        from src.domain.exceptions import TaskNotFoundError

        updated = Task(id="task-999999", description="Updated", status=TaskStatus.COMPLETED)
        with pytest.raises(TaskNotFoundError, match="not found"):
            self.repo.update(updated)

    # Test delete method
    def test_repository_delete_task(self):
        """Test deleting a task."""
        task = Task(id="task-000001", description="To delete", status=TaskStatus.PENDING)
        self.repo.create(task)

        deleted = self.repo.delete("task-000001")
        assert deleted is True

        # Verify it's gone
        assert self.repo.get("task-000001") is None

    def test_repository_delete_non_existent_returns_false(self):
        """Test deleting non-existent task returns False."""
        deleted = self.repo.delete("task-999999")
        assert deleted is False

    # Test filter_by_status method
    def test_repository_filter_by_status_pending(self):
        """Test filtering by PENDING status."""
        task1 = Task(id="task-000001", description="Task 1", status=TaskStatus.PENDING)
        task2 = Task(id="task-000002", description="Task 2", status=TaskStatus.COMPLETED)
        self.repo.create(task1)
        self.repo.create(task2)

        pending = self.repo.filter_by_status(TaskStatus.PENDING)
        assert len(pending) == 1
        assert pending[0].id == "task-000001"

    def test_repository_filter_by_status_completed(self):
        """Test filtering by COMPLETED status."""
        task1 = Task(id="task-000001", description="Task 1", status=TaskStatus.PENDING)
        task2 = Task(id="task-000002", description="Task 2", status=TaskStatus.COMPLETED)
        self.repo.create(task1)
        self.repo.create(task2)

        completed = self.repo.filter_by_status(TaskStatus.COMPLETED)
        assert len(completed) == 1
        assert completed[0].id == "task-000002"

    def test_repository_filter_by_status_empty_result(self):
        """Test filtering with no matching tasks."""
        task = Task(id="task-000001", description="Task 1", status=TaskStatus.PENDING)
        self.repo.create(task)

        completed = self.repo.filter_by_status(TaskStatus.COMPLETED)
        assert completed == []
