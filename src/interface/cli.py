"""
CLI interface for Todo task management system.
Phase I: Command-line interface using argparse (standard library, no external dependencies).
"""
import sys
import argparse

from src.domain.repositories.in_memory import InMemoryTaskRepository
from src.domain.services.task_service import TaskService
from src.lib.identifiers import IdentifierGenerator
from src.domain.models.task import TaskStatus
from src.domain.exceptions import TaskNotFoundError, DuplicateTaskError, InvalidTaskError


def main():
    """Main entry point for CLI interface.

    Supports commands:
    - create: Create a new task
    - list: List all tasks (optionally filtered by status)
    - update: Update task status
    - delete: Delete a task

    All commands print results to stdout in user-friendly format.
    Errors are printed to stderr and process exits with code 1.
    """
    parser = argparse.ArgumentParser(
        description="Todo Task Manager - Phase I CLI",
        epilog="Example: python -m src.interface.cli create 'Buy groceries'"
    )
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        required=True  # Command is required
    )

    # create command
    create_parser = subparsers.add_parser('create', help='Create a new task')
    create_parser.add_argument(
        'description',
        help='Task description (1-256 characters)'
    )

    # list command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument(
        '--status',
        choices=['pending', 'completed'],
        help='Filter by status'
    )

    # update command
    update_parser = subparsers.add_parser('update', help='Update task status')
    update_parser.add_argument('id', help='Task ID (e.g., task-000001)')
    update_parser.add_argument(
        'status',
        choices=['pending', 'completed'],
        help='New status (pending or completed)'
    )

    # delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', help='Task ID (e.g., task-000001)')

    args = parser.parse_args()

    # Initialize service (Phase I: single-instance, in-memory)
    repo = InMemoryTaskRepository()
    id_gen = IdentifierGenerator()
    service = TaskService(repo, id_gen)

    try:
        if args.command == 'create':
            task = service.create_task(args.description)
            print(f"Created: [{task.id}] {task.description} ({task.status.value})")

        elif args.command == 'list':
            status = TaskStatus(args.status) if args.status else None
            tasks = service.list_tasks(status)

            if not tasks:
                print("No tasks found.")
            else:
                for task in tasks:
                    print(f"[{task.id}] {task.description} ({task.status.value})")

        elif args.command == 'update':
            status = TaskStatus(args.status)
            task = service.update_status(args.id, status)
            print(f"Updated: [{task.id}] {task.description} ({task.status.value})")

        elif args.command == 'delete':
            service.delete_task(args.id)
            print(f"Deleted: {args.id}")

    except (ValueError, InvalidTaskError) as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except TaskNotFoundError as e:
        print(f"Not found: {e}", file=sys.stderr)
        sys.exit(1)
    except DuplicateTaskError as e:
        print(f"Conflict: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
