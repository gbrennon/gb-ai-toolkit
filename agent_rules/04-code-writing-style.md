# Code Writing Style

Rules for writing readable, self-documenting code.

## No Comments — Use Expressive Names

- Never write inline comments inside functions or methods
- Instead, make the code self-documenting through expressive names for:
  - Constants
  - Variables
  - Functions and methods
  - Classes
  - Parameters and return types
- A well-named identifier eliminates the need for `# explanation` comments

## Docstrings That Explain Contract or Behavior

Every public function, method, and class must have a docstring.

### For Interfaces / Abstractions (Protocols, ABCs, Ports)
Write a docstring that explains the **contract** — what the caller can expect and what the implementer must guarantee:
- Preconditions (if any)
- Postconditions / guarantees
- Who is responsible for what

### For Implementations
Write a docstring that explains the **behavior** — how the implementation fulfills the contract:
- What this specific implementation does
- Any relevant side effects or resource usage
- Why this approach was chosen (if non-obvious)

### Format
Use the project's standard docstring format (reStructuredText, Google, NumPy, or plain — follow what the codebase already uses).
