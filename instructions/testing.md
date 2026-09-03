## Testing

Tests are first-class citizens. Apply these rules consistently.

**General**: Every new public method or class must come with corresponding tests. Write
tests before or alongside implementation (TDD/BDD mindset). Tests must be fast, isolated,
repeatable, self-validating, and timely (F.I.R.S.T).

**Testability**: Design production code so behavior can be tested through explicit inputs and dependencies.
Do not introduce special production-only paths, test hooks, or test-specific abstractions solely to make code testable.

**Test Design**: Follow Arrange / Act / Assert (AAA) structure in every test. Aim for one
logical assertion per test — a test should have one reason to fail. Name tests
descriptively using the pattern: `<action>_when_<scenario>_then_<result>`. Use test
doubles (mocks, stubs, fakes, spies) to isolate the unit under testl infrastructure and presentation layers should
rely in fixture that was made with a real world interaction to create them so tests really simulate real world.

**Coverage**: Aim for high coverage on domain and application layers. Do not sacrifice test
quality for coverage numbers. Explicitly cover edge cases, boundary conditions, and
error/exception paths.
