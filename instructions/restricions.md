## Absolute Restrictions

- Don't use emojis
- Only write en-us content
- When doing a conventional commit show user and ask for confirmation before doing it.
- Use expressive conventional commits(`<type>(<scope>): <description>`)
- You should do a single commit per file.
- Dont skip pre-git hooks like pre-commit, pre-push, etc

## Never do

- Never instantiate infrastructure dependencies directly inside domain or application services.
- Never skip or mock out tests to make code pass faster.
- Never mock dependency in infrastructure or presentation layers.
- Never produce untestable code (hidden static dependencies, `new` inside business logic,
  global mutable state).
- Never use God classes, God functions, anti-patterns or principle violations.
- Never suggest inheritance where composition is more appropriate.
- Never use ignore comments to rules, types or tests.
