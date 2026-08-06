# Test Writing Style

Rules for writing tests that are not biased, well-structured and well-written.
No comments, expressive names only.
You should use expressive names for classes,tests, params and methods like high-quality code that is self-documenting thorugh expressive names.

## What to test

You should test behavior only.
Don't test implementation.
Test should assert what tested code returns in a given scenario and not if it calls some method.

### Testing rules

Tests don't have logic. They should be simple.
Test should excercise code in all possible scenarios.
When writing unit tests you can mock injectable dependencies but not in code that have external dependencies.
Don't mock what you don't own, you should write integration test and inject fake classes that cover a single scenario per class.
If you have to simulate a scenarioo in which HTTP response contains 400 status code you should have a stub class to have a fake scenario that cover this.
