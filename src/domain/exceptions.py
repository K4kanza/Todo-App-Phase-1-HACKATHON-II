"""
Custom exceptions for Todo task management system.
"""


class TaskNotFoundError(Exception):
    """Raised when a task with the specified ID does not exist."""
    pass


class DuplicateTaskError(Exception):
    """Raised when attempting to create a task with a duplicate ID."""
    pass


class InvalidTaskError(Exception):
    """Raised when task validation fails (e.g., empty description)."""
    pass
