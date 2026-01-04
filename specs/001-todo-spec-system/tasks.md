---

description: "Implementation tasks for Evolution of Todo - Core Task Management"
---

# Tasks: Evolution of Todo - Core Task Management

**Input**: Design documents from `/specs/001-todo-spec-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included based on contract test specifications in contracts/task-service.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths below follow plan.md structure: src/domain/, src/interface/, src/lib/, tests/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per plan.md (src/domain/models, src/domain/repositories, src/domain/services, src/interface, src/lib, tests/contract, tests/integration, tests/unit)
- [X] T002 [P] Create requirements.txt with pytest>=7.4.0
- [X] T003 [P] Create pytest.ini configuration file
- [X] T004 [P] Create README.md with project overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create custom exceptions in src/domain/exceptions.py (TaskNotFoundError, DuplicateTaskError, InvalidTaskError)
- [X] T006 Create TaskRepository abstract base class interface in src/domain/repositories/base.py with all required methods (create, get, list, update, delete, filter_by_status)
- [X] T007 [P] Create IdentifierGenerator class in src/lib/identifiers.py with next_id() method returning format "task-{number:06d}"
- [X] T008 [P] Create InMemoryTaskRepository implementation in src/domain/repositories/in_memory.py implementing TaskRepository with Dict[str, Task] storage
- [X] T009 Create empty __init__.py files in src/domain/, src/domain/models/, src/domain/repositories/, src/domain/services/, src/interface/, src/lib/, tests/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and List Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks and view complete task list

**Independent Test**: Create a task with description and retrieve the task list to verify the task appears with correct ID, description, and pending status

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Contract test for create_task in tests/contract/test_task_service.py (test_create_task_generates_unique_id)
- [X] T011 [P] [US1] Contract test for create_task in tests/contract/test_task_service.py (test_create_task_initializes_pending_status)
- [X] T012 [P] [US1] Contract test for list_tasks in tests/contract/test_task_service.py (test_list_tasks_returns_all_tasks)
- [X] T013 [P] [US1] Unit test for Task entity in tests/unit/test_task.py (test_task_validation_empty_description)
- [X] T014 [P] [US1] Unit test for Task entity in tests/unit/test_task.py (test_task_validation_description_length)
- [X] T015 [P] [US1] Unit test for InMemoryTaskRepository in tests/unit/test_in_memory_repository.py (test_repository_create_task)
- [X] T016 [P] [US1] Unit test for InMemoryTaskRepository in tests/unit/test_in_memory_repository.py (test_repository_list_tasks)
- [X] T017 [P] [US1] Unit test for TaskService in tests/unit/test_task_service.py (test_service_create_task)
- [X] T018 [P] [US1] Integration test for create and list workflow in tests/integration/test_task_workflow.py (test_create_and_list_workflow)

### Implementation for User Story 1

- [X] T019 [P] [US1] Create TaskStatus enum in src/domain/models/task.py with PENDING and COMPLETED values
- [X] T020 [P] [US1] Create Task frozen dataclass in src/domain/models/task.py with id, description, status fields and __post_init__ validation (FR-010)
- [X] T021 [US1] Implement TaskService.__init__ in src/domain/services/task_service.py with repository and id_generator injection
- [X] T022 [US1] Implement TaskService.create_task method in src/domain/services/task_service.py generating ID via id_gen.next_id(), creating Task with PENDING status, persisting via repo.create (FR-001, FR-002, FR-003)
- [X] T023 [US1] Implement TaskService.list_tasks method in src/domain/services/task_service.py with optional status_filter parameter calling repo.list() or repo.filter_by_status (FR-004)
- [X] T024 [US1] Implement CLI 'create' command in src/interface/cli.py accepting description argument, calling service.create_task, printing result format (FR-001)
- [X] T025 [US1] Implement CLI 'list' command in src/interface/cli.py calling service.list_tasks, iterating and printing all tasks (FR-004)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Tasks as Completed (Priority: P2)

**Goal**: Enable users to update task status between pending and completed

**Independent Test**: Create a task, mark it as completed, verify status changed; mark it back to pending, verify status reverted

### Tests for User Story 2

- [X] T026 [P] [US2] Contract test for update_status in tests/contract/test_task_service.py (test_update_status_from_pending_to_completed) - FR-006
- [X] T027 [P] [US2] Contract test for update_status in tests/contract/test_task_service.py (test_update_status_from_completed_to_pending) - FR-007
- [X] T028 [P] [US2] Unit test for TaskService in tests/unit/test_task_service.py (test_service_update_status)
- [X] T029 [P] [US2] Integration test for status update workflow in tests/integration/test_task_workflow.py (test_update_status_workflow)

### Implementation for User Story 2

- [X] T030 [US2] Implement TaskService.update_status method in src/domain/services/task_service.py calling get_task to retrieve existing task, creating new Task instance with updated status, calling repo.update, returning updated task (FR-006, FR-007)
- [X] T031 [US2] Implement CLI 'update' command in src/interface/cli.py accepting id and status arguments, calling service.update_status, printing updated task

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Enable users to remove tasks from the task list

**Independent Test**: Create multiple tasks, delete one by ID, verify it's removed from list; attempt to delete non-existent ID, verify error handling

### Tests for User Story 3

- [X] T032 [P] [US3] Contract test for delete_task in tests/contract/test_task_service.py (test_delete_task_removes_task) - FR-008
- [X] T033 [P] [US3] Contract test for operations with non-existent tasks in tests/contract/test_task_service.py (test_operations_reject_non_existent_task) - FR-012
- [X] T034 [P] [US3] Unit test for TaskService in tests/unit/test_task_service.py (test_service_delete_task)
- [X] T035 [P] [US3] Integration test for delete workflow in tests/integration/test_task_workflow.py (test_delete_workflow)

### Implementation for User Story 3

- [X] T036 [US3] Implement TaskService.delete_task method in src/domain/services/task_service.py calling get_task to verify existence, calling repo.delete, returning None (FR-008)
- [X] T037 [US3] Implement CLI 'delete' command in src/interface/cli.py accepting id argument, calling service.delete_task, printing confirmation

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Filter Tasks by Status (Priority: P4)

**Goal**: Enable users to view only pending or only completed tasks

**Independent Test**: Create tasks with mixed statuses, apply filter for pending, verify only pending shown; apply filter for completed, verify only completed shown

### Tests for User Story 4

- [X] T038 [P] [US4] Contract test for list_tasks with status filter in tests/contract/test_task_service.py (test_list_tasks_filters_by_status) - FR-009
- [X] T039 [P] [US4] Unit test for TaskService in tests/unit/test_task_service.py (test_service_list_tasks_with_filter)
- [X] T040 [P] [US4] Integration test for filter workflow in tests/integration/test_task_workflow.py (test_filter_workflow)

### Implementation for User Story 4

- [X] T041 [US4] Extend CLI 'list' command in src/interface/cli.py to accept optional --status argument, passing TaskStatus enum to service.list_tasks (FR-009)

**Checkpoint**: All 4 user stories should be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T042 [P] Add performance benchmark test for 10,000 tasks in tests/integration/test_task_workflow.py to verify SC-006
- [X] T043 [P] Create performance benchmark test for create task under 3 seconds in tests/integration/test_task_workflow.py to verify SC-001
- [X] T044 [P] Create performance benchmark test for list 100 tasks under 1 second in tests/integration/test_task_workflow.py to verify SC-002
- [X] T045 [P] Create performance benchmark test for update status under 1 second in tests/integration/test_task_workflow.py to verify SC-003
- [X] T046 [P] Run all contract tests and verify 100% pass rate to verify SC-004
- [X] T047 Update quickstart.md validation checklist with implementation completion status
- [X] T048 Add type checking configuration (mypy.ini) to enforce explicit typing
- [X] T049 Run quickstart.md verification checklist to confirm all FRs and SCs satisfied

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3 → P4)
  - Each story builds on previous CLI structure but is independently testable
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses existing CLI structure from US1 but is independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses existing CLI structure from US1/US2 but is independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Modifies existing CLI 'list' command from US1 but is independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD approach)
- Models before services
- Services before endpoints/CLI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T002, T003, T004) can run in parallel
- All Foundational tasks (T007, T008, T009) can run in parallel within Phase 2 (after T005, T006)
- Once Foundational phase completes, test tasks for each user story (marked [P]) can run in parallel
- Different user stories can be worked on sequentially in priority order (P1 → P2 → P3 → P4)
- Performance benchmark tests in Phase 7 (T042-T045) can run in parallel
- Polish tasks (T047-T048) can run in parallel after T046

---

## Parallel Example: User Story 1

```bash
# Launch all contract tests for User Story 1 together:
Task: "Contract test for create_task in tests/contract/test_task_service.py (test_create_task_generates_unique_id)"
Task: "Contract test for create_task in tests/contract/test_task_service.py (test_create_task_initializes_pending_status)"
Task: "Contract test for list_tasks in tests/contract/test_task_service.py (test_list_tasks_returns_all_tasks)"

# Launch all unit tests for User Story 1 together:
Task: "Unit test for Task entity in tests/unit/test_task.py (test_task_validation_empty_description)"
Task: "Unit test for Task entity in tests/unit/test_task.py (test_task_validation_description_length)"
Task: "Unit test for InMemoryTaskRepository in tests/unit/test_in_memory_repository.py (test_repository_create_task)"
Task: "Unit test for InMemoryTaskRepository in tests/unit/test_in_memory_repository.py (test_repository_list_tasks)"
Task: "Unit test for TaskService in tests/unit/test_task_service.py (test_service_create_task)"

# Launch all models for User Story 1 together:
Task: "Create TaskStatus enum in src/domain/models/task.py with PENDING and COMPLETED values"
Task: "Create Task frozen dataclass in src/domain/models/task.py with id, description, status fields and __post_init__ validation"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T010-T025)
4. **STOP and VALIDATE**: Test User Story 1 independently using CLI commands
5. Deploy/demo if ready - this is MVP (create and list tasks)

### Incremental Delivery

1. Complete Setup (Phase 1) + Foundational (Phase 2) → Foundation ready
2. Add User Story 1 (Phase 3) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Phase 4) → Test independently → Deploy/Demo (can mark tasks complete)
4. Add User Story 3 (Phase 5) → Test independently → Deploy/Demo (can delete tasks)
5. Add User Story 4 (Phase 6) → Test independently → Deploy/Demo (can filter tasks)
6. Complete Polish (Phase 7) → Full Phase I system ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup (Phase 1) + Foundational (Phase 2) together
2. Once Foundational is done, work sequentially in priority order:
   - Developer A: User Story 1 (P1)
   - Developer B: User Story 2 (P2) - after US1 tests pass
   - Developer C: User Story 3 (P3) - after US2 tests pass
3. Stories complete and integrate independently
4. Polish phase (Phase 7) can be parallelized across team

---

## Summary

- **Total Tasks**: 49 tasks
- **Tasks per User Story**:
  - User Story 1 (P1): 16 tasks (9 tests + 7 implementation)
  - User Story 2 (P2): 6 tasks (4 tests + 2 implementation)
  - User Story 3 (P3): 6 tasks (4 tests + 2 implementation)
  - User Story 4 (P4): 4 tasks (3 tests + 1 implementation)
- **Setup Phase**: 4 tasks
- **Foundational Phase**: 5 tasks
- **Polish Phase**: 8 tasks

**Parallel Opportunities**:
- 21 tasks marked [P] can run in parallel (42% parallelizable)
- Test writing is highly parallelizable within each story
- Performance benchmarks in Polish phase are parallelizable

**Independent Test Criteria per Story**:
- **US1**: Create task, list tasks → verify task appears with correct ID, description, pending status
- **US2**: Create task, update status to completed → verify status changed; update to pending → verify reverted
- **US3**: Create multiple tasks, delete one → verify removed; delete non-existent → verify error
- **US4**: Create tasks with mixed statuses, filter by pending/completed → verify correct subset shown

**Suggested MVP Scope**: User Story 1 only (T001-T025) - enables creating and listing tasks, delivers core value immediately

**Format Validation**: ✅ ALL 49 tasks follow checklist format with checkbox, ID, [P] marker where applicable, [Story] label for user story tasks, and file paths

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability to spec.md
- Each user story should be independently completeable and testable
- Verify tests fail before implementing (TDD approach enforced)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All FRs (FR-001 to FR-014) mapped to implementation tasks
- All SCs (SC-001 to SC-006) verified through test tasks and benchmarks
