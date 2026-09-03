## Absolute Restrictions

- Don't use emojis, only plain text unless its requested
- Only write en-us content
- When doing a conventional commit show user and ask for confirmation before doing it.
- Use expressive conventional commits(`<type>(<scope>): <description>`)
- You should do a single commit per file.
- Dont skip pre-git hooks like pre-commit, pre-push, etc

## Never do

* Never implement functions or methods with cyclomatic complexity greater than 10.
* Never increase complexity to avoid introducing an appropriate abstraction or decomposition.
- Never instantiate infrastructure dependencies directly inside domain or application services.
- Never skip git hooks
- Never skip or mock out tests to make code pass faster.
- Never mock dependency in infrastructure or presentation layers.
- Never mock external dependencies. Don't mock what you don't own.
- Never produce untestable code (hidden static dependencies, `new` inside business logic,
  global mutable state).
* Never hide dependencies behind global state, service locators, or implicit runtime lookups.
* Never couple business logic directly to external frameworks, libraries, protocols, or infrastructure.
* Never use `Any`, untyped escape hatches, or equivalent mechanisms to bypass type safety.
- Never use God classes, God functions, anti-patterns or principle violations.
- Never suggest inheritance where composition is more appropriate.
- Never use ignore comments to rules, types or tests.
