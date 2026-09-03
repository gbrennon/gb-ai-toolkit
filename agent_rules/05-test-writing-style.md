# Test Writing Style

Rules for writing tests that are not biased, well-structured and well-written.
No comments, expressive names only.
You should use expressive names for classes,tests, params and methods like high-quality code that is self-documenting thorugh expressive names.

## What to test

You should test behavior only.
Don't test implementation.
Test should assert what tested code returns in a given scenario and not if it calls some method.

### Testing rules

If you are going to modificate behavior you should write test first.
Tests shouldn't have logic. They should be simple.
Test should excercise code in all possible scenarios.
When writing unit tests you can mock injectable dependencies but in code that have external dependencies you should write integration tests that use fake classes to represent interaction.
Don't mock what you don't own, you should write integration test and inject fake classes that cover a single scenario per class.
If you have to simulate a scenarioo in which HTTP response contains 400 status code you should have a stub class to have a fake/stub class for that scenario that cover this.
Keep test rule high
