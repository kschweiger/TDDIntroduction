# 1. Getting started

## Concept



The main propose of following a test-driven development schema is to ensure good code quality and to get code that is stable, predictable and well maintainable.
This is accomplished by:

1. Ensuing all code works as intended
2. Factorized code is a side product when following the test-driven approach

The value of 1. is instantly clear. Since testing a function does exactly this, only that in a test-driven approach this is done on a much more systematic level than just testing the code after writing it is. In addition this systematic approach leads to a situation, where changes in some part of the code that effect other functions are immediately noticeable.
The second item is less clear immediately. The argument here is that writing testing is much easier (or even possible) if the code factorizes functions in a meaning full way.

An important additional concept is, to write the test before writing the function to be tested!

## Terminology
Test-driven development comes with a lot of terminology that the reader should be familiar with. Different kinds of tests like **unit-tests** and **integration-tests**. 
For modern programming languages, there are **testing frameworks** (or test runner), that help organizing, automating and formalizing tests. For python, commonly used ones are `unittest` (included in the standard library) or `pytest`.

### Unit-test
The most basic way of testing is the unit-test. It denotes a test that tests a single function.     
The idea of a unit-test is that a function is called with a defined input (called the **test step**) and the return value is compared to the expected output (called the **test assertion**). 

### Integration-test
An integration-test, tests if different components of your application interact in the expected way. If the integration-test fails, a good set of unit-test can help with finding the problem quickly.

### Testing frameworks

#### unittest 
The unittest module is part of the python standard library since 2.1 and can be used in almost any installation without problems. Setting a tests with unittest requires 

- To put your test into class (inheriting from `unittest.TestCase`) methods 
- Use a set of special assertion methods from the `unittest.TestCase` module instead of the built-in assertion.


#### pytest
[Pytest](https://pytest.org/en/latest/) builds on the foundations of `unittest` (and works very similar) but simplifies how tests have to be written and evaluated. In contrast to `unittest` the tests in `pytest` do not need 

- to be be a method of a `unittest.TestCase`-type class or 
- use the special assertion methods.

Other great features are:

- tests are functions just have to start with `test_`
- Executing `pytest` form the CLI offers nice output 
- A large number of additional plugins

### Other commonly used terms

#### coverage
For coverage the test runner records with lines of the code are actually run during the tests. The ratio between executed lines and all lines of the code is called the coverage. Ideally to coverage of your project should be 100%.

#### mock
A mock is a object that acts as a dependency with defined attributes. This is e.g. required if your test needs some input from a third party dependency which you don't want to test. More on this will be covered in the [advanced topics section](advanced_topics.md).

#### side effect
Often looking at the return value is not the only thing a test need to check. A piece of code will often alter e.g. some class attribute. This is called a **side effect**.

#### Code refactoring
This denotes to process of taking existing code (like a function) and restructuring it w/o changing the external behavior. This is usually achieved by moving parts of the code to a function or method. Generally this process leads to code that is better readable and reduces complexity. In the context of test-driven development this additionally leads to tests with less dependencies, since each "sub-functon" can be tested (or more importantly mocked) on it own.



