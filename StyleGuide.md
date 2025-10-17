# Python Style Guide

This style guide establishes coding standards for our COMP333 project.

## 1. Comment Style

### Block Comments
- Use docstrings `"""` immediately after the function declaration
- Follow [PEP 257](https://peps.python.org/pep-0257/) format
- They should describe the function's purpose, parameters, and return values

```python
def halve_number(x: int) -> float:
    """Return half of the given number.
    
    Arguments:
        x: A numeric value to be divided by 2
        
    Returns:
        float: The result of x divided by 2 as a floating-point number
    """
    return x / 2
```

### Inline Comments
- Follow [PEP 8](https://peps.python.org/pep-0008/#inline-comments) format
- Notably, they should be separated by at least two spaces from the statement and begin with `#` and a single space
- Avoid stating the obvious, but supplement with meaningful intent

## 2. Naming

### Variables
- Use "snake_case" for all variables: lowercase and underscores
- Use descriptive nouns or noun phrases
- Names to avoid:
    - Single-character names except for specific cases:
        - Loop counters: `i`, `j`, `k`
        - `e` as an exception identifier in `try/except` statements
        - `f` as a file handle when using `with` statements
    - Overly similar function names to create distinction

### Functions
- snake_case for all functions
- Start with action verbs
- Be specific about what the function does

```python
def calculate_area(length: float, width: float) -> float:
def convert_to_celsius(fahrenheit: float) -> float:
def is_even(number: int) -> bool:
```

### Classes
- **PascalCase** (CapitalizedWords)
- Use descriptive nouns

```python
class Student:
class WhiteDwarf:
```

### Constants
- **UPPER_SNAKE_CASE**
- Define at module level

```python
MAX_POTENTIAL_VALUE = 100
DEFAULT_TIMEOUT = 60
API_URL = "https://insertapihere.com"
```

## 3. Cohesion and Coupling

### Increasing Cohesion
- Definition: the degree of functional relatedness of methods and data structures within a single class or module
- High cohesion is desirable
- First, we factor the main problem into its subproblems
- We create classes/modules where each of its elements are related to and belong to each other

### Reducing Coupling
- Definition: the degree to which two classes/modules interact with one another
- Low coupling is desirable
- Use abstractions rather than concrete implementations

### Why?
- This allows us to:
    - Reason within the boundaries of a single class/module rather than the functionality of the program as a whole
    - Work on different parts of the codebase independently as changing a single class/module won't affect the others
    - Locate bugs easily because classes/modules are organized by relatedness

## 4. Branching Norms

### Naming
- Use lowercase characters, numerals, and hyphens to create descriptive names for each branch
- Use prefix convention that describe the purpose of each branch
- Prefix tokens:
    - feature/ for new features
    - hotfix/ for high-priority fixes
    - bugfix/ for non-critical bug fixes and experimentation
    - docs/ for any changes in documentation
- Include an issue ID to track history
- Some examples:
    - `feature/ 1-data-import`
    - `feature/ 77-graph-visualization`
    - `bugfix/ 24-fix-unit-test`

### Workflow Guidelines
1. Create a branch from the latest version of `main`
2. Keep branches focused and short-lived: maximum of 2 weeks
3. Make regular commits and sync regularly with `main` to avoid conflicts
4. Push changes to the remote repository

### Merge Conditions
1. At least one team member must review and approve the merge request
2. Testing requirements:
    - Verify that all unit tests pass
    - Include appropriate unit tests for any new features
    - Verify the feature works as intended
3. Coding Standards:
    - Follows all style guidelines in this document
    - Ample documentation using docstrings and comments
    - No merge conflicts with `main`
4. Update relevant documentation such as `README` if the changes affect user-facing functionality

### Merge Process
1. Create a pull request from your feature branch to `main`
2. Request review from at least one team member
3. Address any feedback or requested changes
4. Once approved and all conditions are met, the reviewer may merge
5. Delete the feature branch after successful merge

## 5. Additional Resources

### Core Python Standards
- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
