## Architecture & Design Guidelines

- Favor composition over inheritance.
- Program to interfaces and abstractions, never to implementations.
* Make dependencies explicit through constructors or function parameters.
* Keep dependency direction pointing toward abstractions and stable business rules, never toward implementation details.
- Keep domain and application logic free of infrastructure concerns (no HTTP, DB, or I/O in domain classes).
- Apply layered or hexagonal architecture: separate domain, application, infrastructure, and presentation.
- Prefer immutable data structures and pure functions where possible.
- Avoid anemic domain models — domain objects must carry behavior, not just data.
- Keep functions and methods small and focused (single level of abstraction per function).
* Each function or method should have one clear responsibility and one primary reason to change.
* Prefer decomposing complex behavior into cohesive functions over adding conditionals, flags, or branching to an existing function.
- Use meaningful, intention-revealing names for everything.
- Avoid premature optimization — write clear code first.
- Limit function parameter count; use parameter objects when more than 3 parameters.
- Avoid deep nesting — prefer early returns and guard clauses.
- Handle errors explicitly; never silently swallow exceptions.
- Keep cyclomatic complexity of every function or method at 10 or less.
- Treat cyclomatic complexity above 10 as a design problem that must be refactored before implementation is considered complete.
