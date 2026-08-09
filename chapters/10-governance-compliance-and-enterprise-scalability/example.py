# reusable_workflow.py - Simulates a reusable workflow for CI/CD.

def lint_code(repo_name):
    """Simulates linting code for a given repository."""
    print(f"[{repo_name}] Linting code... Done.")
    return True

def run_tests(repo_name, test_suite="unit"):
    """Simulates running tests for a given repository."""
    print(f"[{repo_name}] Running {test_suite} tests... Done.")
    return True

def deploy_to_staging(repo_name):
    """Simulates deploying the application to a staging environment."""
    print(f"[{repo_name}] Deploying to staging... Done.")
    return True

def security_scan(repo_name):
    """Simulates running a security scan."""
    print(f"[{repo_name}] Running security scan... Done.")
    return True

# enterprise_policy.py - Simulates an organization-wide policy enforcement.

class ComplianceError(Exception):
    """Custom exception for compliance violations."""
    pass

def enforce_enterprise_workflow(repo_name, required_steps):
    """
    Enforces a standardized CI/CD workflow across repositories.

    Args:
        repo_name (str): The name of the repository.
        required_steps (list): A list of required functions (steps) to execute.

    Raises:
        ComplianceError: If any required step fails.
    """
    print(f"\n--- Enforcing enterprise workflow for: {repo_name} ---")
    for step_func in required_steps:
        try:
            if not step_func(repo_name):
                raise ComplianceError(f"Step '{step_func.__name__}' failed for {repo_name}.")
        except Exception as e:
            raise ComplianceError(f"Error during step '{step_func.__name__}' for {repo_name}: {e}")
    print(f"--- Workflow enforcement for {repo_name} successful. ---")


if __name__ == "__main__":
    # Define the enterprise-mandated CI/CD workflow steps
    enterprise_standard_workflow = [
        lint_code,
        run_tests,
        security_scan,
        deploy_to_staging,
    ]

    # Simulate different repositories adopting (or not) the reusable workflow
    repositories = ["frontend-app", "backend-service", "data-pipeline"]

    for repo in repositories:
        try:
            enforce_enterprise_workflow(repo, enterprise_standard_workflow)
        except ComplianceError as e:
            print(f"Compliance violation detected for {repo}: {e}")

    # Example of a repository with a custom test suite
    print("\n--- Simulating a repository with a custom test suite ---")
    try:
        enforce_enterprise_workflow("mobile-app", [
            lint_code,
            lambda r: run_tests(r, test_suite="e2e"), # Custom step within policy
            security_scan
        ])
    except ComplianceError as e:
        print(f"Compliance violation detected for mobile-app: {e}")
