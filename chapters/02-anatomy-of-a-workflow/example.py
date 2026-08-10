# This script simulates a simplified GitHub Actions workflow.
# It demonstrates the core concepts: events, jobs, and steps.

# --- 1. Event Simulation ---
# In GitHub Actions, events trigger workflows.
# Here, we simulate a 'push' event to a 'main' branch.
simulated_event = {
    "type": "push",
    "branch": "main",
    "commit_message": "feat: Add new feature"
}

def check_event_trigger(event_config, actual_event):
    """
    Checks if the actual event matches the workflow's configured trigger.
    """
    if actual_event["type"] == event_config["on"]:
        if "branches" in event_config and \
           actual_event["branch"] not in event_config["branches"]:
            return False
        return True
    return False

# --- 2. Workflow Definition (Simplified YAML-like Structure) ---
workflow_config = {
    "name": "CI Pipeline",
    "on": {
        "push": {
            "branches": ["main", "develop"]
        }
    },
    "jobs": {
        "build_and_test": {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v4"},
                {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
                {"name": "Run tests", "run": "pytest tests/"}
            ]
        }
    }
}

# --- 3. Workflow Execution Simulation ---
def execute_workflow(workflow, event):
    """
    Simulates the execution of a GitHub Actions workflow.
    """
    print(f"--- Workflow: {workflow['name']} ---")
    print(f"Simulating event: {event['type']} on branch {event['branch']}")

    if not check_event_trigger(workflow["on"], event):
        print("Event did not trigger the workflow. Exiting.")
        return

    print("Event matched trigger. Starting jobs...")
    for job_name, job_config in workflow["jobs"].items():
        print(f"\n--- Running Job: {job_name} on {job_config['runs-on']} ---")
        for step in job_config["steps"]:
            print(f"  Executing Step: {step['name']}")
            # In a real scenario, 'uses' would run an action, 'run' would execute a shell command.
            # Here, we just print the action/command.
            if "uses" in step:
                print(f"    (Action: {step['uses']})")
            elif "run" in step:
                print(f"    (Command: {step['run']})")
            # Simulate a successful step for this example
            print("    Status: Success")
    print("\n--- Workflow Completed ---")

# --- Run the simulation ---
execute_workflow(workflow_config, simulated_event)

# Example of an event that won't trigger the workflow
simulated_event_pr = {
    "type": "pull_request",
    "branch": "feature-x",
    "commit_message": "feat: Add pull request feature"
}
# execute_workflow(workflow_config, simulated_event_pr) # Uncomment to see non-triggering event

# Example of a push to a non-monitored branch
simulated_event_other_branch = {
    "type": "push",
    "branch": "feature-branch",
    "commit_message": "feat: Some dev work"
}
# execute_workflow(workflow_config, simulated_event_other_branch) # Uncomment to see non-triggering branch
