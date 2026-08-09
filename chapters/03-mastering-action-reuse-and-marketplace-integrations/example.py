# This script demonstrates how to integrate and use a community-driven
# GitHub Action (if it were a Python function) to perform a common task:
# linting Python code.

# In a real GitHub Actions workflow, you would use 'uses: community/action@v1'
# to call such an action directly. Here, we simulate its behavior with a Python function.

import os

def run_pylint(file_path: str) -> bool:
    """
    Simulates a 'community/pylint-action@v1' GitHub Action.
    Checks a Python file for linting errors using a simplified pylint-like logic.
    Returns True if no errors, False otherwise.
    """
    print(f"--- Simulating pylint-action for {file_path} ---")
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False

    with open(file_path, 'r') as f:
        content = f.read()

    errors_found = []

    # Simplified linting rules:
    # 1. Check for 'print(' statements (often discouraged in production code)
    if "print(" in content:
        errors_found.append("Found 'print()' statement.")
    # 2. Check for missing docstrings in functions (very basic check)
    if "def " in content and '"""' not in content:
        errors_found.append("Possible missing docstring in function.")
    # 3. Check for 'TODO' comments (as a reminder)
    if "TODO" in content:
        errors_found.append("Found 'TODO' comment.")

    if errors_found:
        print("Linting errors found:")
        for error in errors_found:
            print(f"- {error}")
        return False
    else:
        print("No linting errors found.")
        return True

def main():
    # Create a dummy Python file to lint
    test_file_name = "example_code.py"
    with open(test_file_name, "w") as f:
        f.write("""
import os

def my_function():
    # TODO: Add more features
    print("Hello, world!") # This will be flagged by our linter
    pass

class MyClass:
    def __init__(self):
        pass # This function has no docstring, might be flagged

if __name__ == "__main__":
    my_function()
""")

    print(f"Created '{test_file_name}' for testing.")

    # Simulate a GitHub Actions workflow step using the community action
    print("\n--- GitHub Actions Workflow Step: Linting Python Code ---")
    linting_successful = run_pylint(test_file_name)

    if linting_successful:
        print("\nWorkflow step: Python linting PASSED.")
    else:
        print("\nWorkflow step: Python linting FAILED. Please fix the issues.")

    # Clean up the dummy file
    os.remove(test_file_name)
    print(f"\nCleaned up '{test_file_name}'.")

if __name__ == "__main__":
    main()
