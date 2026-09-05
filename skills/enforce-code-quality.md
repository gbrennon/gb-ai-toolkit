---
name: enforce-code-quality
description: Set up, run, and enforce code quality policies using the check-code-quality CLI (Lizard complexity + Semgrep structural rules), and refactor violations.
---

# Enforce Code Quality

Enforce quantitative complexity and structural quality standards on all code changes. Zero violations are permitted before claiming work is complete.

## Quality Standards

| Metric / Rule | Threshold | Tool | Rationale |
|---|---|---|---|
| **Cyclomatic Complexity** | CCN $\le$ 5 | Lizard (`-C 5`) | Functions with high branching are hard to reason about, test, and maintain. |
| **Control-flow Nesting** | Depth $\le$ 2 | Semgrep (`nesting.yml`) | Nested loops/conditionals obscure happy-path logic and invite bugs. |
| **Function Length** | Lines $\le$ 50 | Lizard (`-L 50`) | Keeps functions focused on a single abstraction level and responsibility. |
| **Argument Count** | Args $\le$ 5 | Lizard (`-a 5`) | High parameter count signals missing parameter objects or split abstractions. |
| **Strong Types & Hints** | 100% typed | Type checker / Rules | Every signature, return type, and example must be explicitly typed; no `Any`. |
| **Strongly-Typed Generics**| Explicit bounds | Compiler / Type checker | Libraries and shared components must define strongly typed generics, not raw objects. |
| **Never Ignore Rules** | 0 ignore comments | Semgrep (`conventions.yml`) | `# type: ignore`, `#[allow(...)]`, `@ts-ignore` hide code quality misses. |
| **No Generic Setters** | Zero `set_*` methods | Semgrep (`conventions.yml`) | Expose domain behavior and invariants, not raw mutable state. |
| **Field Encapsulation** | No public struct fields | Semgrep (`conventions.yml`) | Public fields leak internal representation and break encapsulation. |
| **No Inline Modules** | Separate files per module | Semgrep (`conventions.yml`) | Enforces one abstraction/contract per file for navigation and cohesion. |
| **Architectural Boundaries** | Domain $\not\to$ Infra/Presentation | Semgrep (`architecture.yml`) | Domain must remain pure and independent of external frameworks. |
---

## Running Quality Checks

### 1. Primary Workflow: `check-code-quality` CLI

Use the dedicated CLI wrapper to run all checks:

```bash
# Scan current directory with default thresholds (CCN <= 5, Length <= 50, Args <= 5)
check-code-quality

# Scan a specific directory
check-code-quality src/

# Initialize project-local .semgrep/ configuration
check-code-quality --init

# Run only complexity or only structural analysis
check-code-quality --only-lizard
check-code-quality --only-semgrep

# Custom thresholds
check-code-quality -C 4 -L 40 -a 4
```

### 2. Manual Fallback Commands

If `check-code-quality` wrapper is not yet installed in `PATH`:

```bash
# Lizard complexity scan
lizard -C 5 -L 50 -a 5 -i 0 .

# Semgrep structural scan (using project rules or bundled config)
semgrep scan --config .semgrep --error .
```

---

## Refactoring Recipes

### Recipe 1: Flattening Nested Control Flow with Guard Clauses

**Violation (Nesting depth 3):**
```rust
fn process_order(order: &Order, user: &User) -> Result<(), OrderError> {
    if user.is_authenticated() {
        if order.has_items() {
            if user.has_sufficient_balance(order.total()) {
                execute_order(order)?;
            }
        }
    }
    Ok(())
}
```

**Refactored (Guard clauses, depth 1):**
```rust
fn process_order(order: &Order, user: &User) -> Result<(), OrderError> {
    if !user.is_authenticated() {
        return Err(OrderError::Unauthenticated);
    }
    if !order.has_items() {
        return Err(OrderError::EmptyOrder);
    }
    if !user.has_sufficient_balance(order.total()) {
        return Err(OrderError::InsufficientFunds);
    }

    execute_order(order)
}
```

---

### Recipe 2: Extracting Cohesive Helpers to Lower Cyclomatic Complexity

When cyclomatic complexity exceeds 5, extract distinct phases into single-responsibility helper functions.

**Violation (Complexity CCN = 7):**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    type: str
    is_admin: bool = False
    field: str | None = None

def handle_event(event: Event) -> None:
    if event.type == "CREATED":
        if event.is_admin:
            send_admin_welcome(event)
        else:
            send_user_welcome(event)
    elif event.type == "UPDATED":
        if event.field == "email":
            verify_email(event)
        elif event.field == "password":
            reset_password(event)
    elif event.type == "DELETED":
        archive_account(event)
```

**Refactored (Dispatched handlers with strongly-typed generics, each CCN $\le$ 2):**
```python
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Generic, TypeVar

@dataclass(frozen=True)
class Event:
    type: str
    is_admin: bool = False
    field: str | None = None

TEvent = TypeVar("TEvent", bound=Event)

class EventDispatcher(Generic[TEvent]):
    """Dispatches domain events to dedicated single-responsibility handlers."""

    def __init__(self, handlers: Mapping[str, Callable[[TEvent], None]]) -> None:
        self._handlers: Mapping[str, Callable[[TEvent], None]] = handlers

    def dispatch(self, event: TEvent) -> None:
        handler: Callable[[TEvent], None] | None = self._handlers.get(event.type)
        if handler is not None:
            handler(event)

def handle_created(event: Event) -> None:
    if event.is_admin:
        send_admin_welcome(event)
        return
    send_user_welcome(event)

def handle_updated(event: Event) -> None:
    if event.field == "email":
        verify_email(event)
    elif event.field == "password":
        reset_password(event)

def handle_deleted(event: Event) -> None:
    archive_account(event)
```
---

### Recipe 3: Replacing Setters with Domain Behavior

**Violation (Generic setter exposes mutable state):**
```rust
impl Subscription {
    pub fn set_status(&mut self, status: Status) {
        self.status = status;
    }

    pub fn set_canceled_at(&mut self, timestamp: DateTime<Utc>) {
        self.canceled_at = Some(timestamp);
    }
}
```

**Refactored (Explicit domain behaviors with invariant protection):**
```rust
impl Subscription {
    pub fn cancel(&mut self, timestamp: DateTime<Utc>) -> Result<(), SubscriptionError> {
        if self.status == Status::Canceled {
            return Err(SubscriptionError::AlreadyCanceled);
        }
        self.status = Status::Canceled;
        self.canceled_at = Some(timestamp);
        Ok(())
    }

    pub fn activate(&mut self) -> Result<(), SubscriptionError> {
        self.status = Status::Active;
        Ok(())
    }
}
```

---

### Recipe 4: Eliminating Ignore Comments with Strongly-Typed Generics

Ignore comments like `# type: ignore`, `#[allow(...)]`, or `@ts-ignore` hide bugs and broken contracts instead of solving them. Always address the underlying type contract.

**Violation (Suppressing type errors hides invalid contract):**
```python
from typing import Any

class Repository:
    def __init__(self) -> None:
        self._items: dict[str, Any] = {}

    def get(self, item_id: str) -> Any:
        return self._items.get(item_id)

repo = Repository()
item: User = repo.get("u1")  # type: ignore[assignment]
```

**Refactored (Strongly-typed generic contract with compile-time safety):**
```python
from typing import Generic, TypeVar

TEntity = TypeVar("TEntity")

class Repository(Generic[TEntity]):
    """Strongly-typed repository interface with generic entity parameter."""

    def __init__(self) -> None:
        self._items: dict[str, TEntity] = {}

    def get(self, item_id: str) -> TEntity | None:
        return self._items.get(item_id)

    def save(self, item_id: str, entity: TEntity) -> None:
        self._items[item_id] = entity

user_repo: Repository[User] = Repository[User]()
user: User | None = user_repo.get("u1")
```

---

## Verification Before Claiming Done

Always run:
```bash
check-code-quality
```
Confirm the terminal displays:
```
✅ Lizard complexity analysis passed.
✅ Semgrep structural analysis passed.
✅ All code quality checks passed.
```
Before submitting or finalizing any branch or commit.
