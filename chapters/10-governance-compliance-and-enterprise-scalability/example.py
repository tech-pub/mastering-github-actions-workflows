# python_linter.py
import os
import sys

def check_file_for_patterns(filepath, patterns):
    """
    Checks if a file contains any of the specified patterns.
    Returns True if any pattern is found, False otherwise.
    """
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            for pattern in patterns:
                if pattern in content:
                    return True
        return False
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return False

def enforce_workflow_policy(workflow_file, required_jobs, restricted_runners):
    """
    Enforces governance policies on a GitHub Actions workflow file.

    Args:
        workflow_file (str): Path to the GitHub Actions workflow YAML file.
        required_jobs (list): List of job names that must be present.
        restricted_runners (list): List of runner types that are not allowed.

    Returns:
        bool: True if all policies are met, False otherwise.
    """
    print(f"Checking workflow: {workflow_file}")

    # Policy 1: Ensure specific jobs are present (e.g., 'security-scan', 'lint')
    for job in required_jobs:
        if not check_file_for_patterns(workflow_file, [f"  {job}:"]):
            print(f"  Policy Violation: Required job '{job}' is missing.", file=sys.stderr)
            return False

    # Policy 2: Prevent use of restricted runner types (e.g., self-hosted runners without approval)
    for runner in restricted_runners:
        if check_file_for_patterns(workflow_file, [f"  runs-on: {runner}"]):
            print(f"  Policy Violation: Restricted runner '{runner}' found.", file=sys.stderr)
            return False

    print("  All policies met for this workflow.")
    return True

if __name__ == "__main__":
    # Simulate a GitHub Actions workflow file
    # In a real scenario, this would be read from the actual .github/workflows directory
    example_workflow_content = """
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run tests
      run: echo "Running tests..."

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - name: Perform security scan
      run: echo "Scanning for vulnerabilities..."

  deploy:
    runs-on: self-hosted # This would be a restricted runner in many organizations
    steps:
    - name: Deploy application
      run: echo "Deploying application..."
"""

    # Create a dummy workflow file for testing
    workflow_path = "example_workflow.yml"
    with open(workflow_path, "w") as f:
        f.write(example_workflow_content)

    # Define organization-wide policies
    org_required_jobs = ["build", "security-scan"]
    org_restricted_runners = ["self-hosted", "windows-latest"]

    # Enforce policies on the example workflow
    policy_status = enforce_workflow_policy(
        workflow_path, org_required_jobs, org_restricted_runners
    )

    if policy_status:
        print("\nWorkflow passed all governance checks.")
        sys.exit(0)
    else:
        print("\nWorkflow failed governance checks. Manual review required.", file=sys.stderr)
        sys.exit(1)

    # Clean up the dummy file
    os.remove(workflow_path)
