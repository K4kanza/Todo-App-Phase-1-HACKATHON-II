"""
Unit tests for Task entity.
"""
import pytest

from src.domain.models.task import Task, TaskStatus


class TestTaskEntity:
    """Unit tests for Task dataclass."""

    # FR-010: System MUST reject task creation with empty or whitespace-only descriptions
    def test_task_validation_empty_description(self):
        """Empty description raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Task(id="task-000001", description="", status=TaskStatus.PENDING)

    def test_task_validation_whitespace_only_description(self):
        """Whitespace-only description raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Task(id="task-000001", description="   ", status=TaskStatus.PENDING)

    def test_task_validation_description_length(self):
        """Description exceeding 256 characters raises ValueError."""
        with pytest.raises(ValueError, match="cannot exceed 256"):
            Task(
                id="task-000001",
                description="x" * 257,
                status=TaskStatus.PENDING
            )

    def test_task_creation_valid(self):
        """Valid task creation succeeds."""
        task = Task(
            id="task-000001",
            description="Valid task description",
            status=TaskStatus.PENDING
        )
        assert task.id == "task-000001"
        assert task.description == "Valid task description"
        assert task.status == TaskStatus.PENDING

    def test_task_immutable_frozen(self):
        """Task is immutable due to frozen=True."""
        task = Task(
            id="task-000001",
            description="Test task",
            status=TaskStatus.PENDING
        )
        with pytest.raises(Exception):  # frozen dataclass raises error
            task.description = "Modified"
