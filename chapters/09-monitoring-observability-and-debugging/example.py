import time
import random
import json

# Simulate a workflow step's execution with varying success and duration
def run_workflow_step(step_name, fail_rate=0.1, min_duration=0.5, max_duration=2.0):
    start_time = time.time()
    successful = random.random() > fail_rate
    duration = random.uniform(min_duration, max_duration)
    time.sleep(duration)
    end_time = time.time()

    status = "SUCCESS" if successful else "FAILURE"
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(start_time)),
        "step_name": step_name,
        "status": status,
        "duration_seconds": round(duration, 3),
        "message": f"{step_name} completed with status {status}"
    }

    # Simulate logging to a structured format (e.g., JSON for easy parsing)
    print(json.dumps(log_entry))
    return successful, duration

# Simulate a multi-step GitHub Actions workflow
def simulate_github_workflow():
    print("--- Starting Workflow Simulation ---")
    workflow_results = []
    workflow_start = time.time()

    # Step 1: Build Application
    success, duration = run_workflow_step("Build Application", fail_rate=0.05, min_duration=1.0, max_duration=3.0)
    workflow_results.append({"step": "Build Application", "success": success, "duration": duration})
    if not success:
        print("Workflow terminated early due to 'Build Application' failure.")
        return False, workflow_results

    # Step 2: Run Unit Tests
    success, duration = run_workflow_step("Run Unit Tests", fail_rate=0.15, min_duration=2.0, max_duration=5.0)
    workflow_results.append({"step": "Run Unit Tests", "success": success, "duration": duration})
    if not success:
        print("Workflow terminated early due to 'Run Unit Tests' failure.")
        return False, workflow_results

    # Step 3: Deploy to Staging (more prone to failures)
    success, duration = run_workflow_step("Deploy to Staging", fail_rate=0.2, min_duration=3.0, max_duration=7.0)
    workflow_results.append({"step": "Deploy to Staging", "success": success, "duration": duration})
    if not success:
        print("Workflow terminated early due to 'Deploy to Staging' failure.")
        return False, workflow_results

    # Step 4: Integration Tests
    success, duration = run_workflow_step("Integration Tests", fail_rate=0.1, min_duration=2.5, max_duration=6.0)
    workflow_results.append({"step": "Integration Tests", "success": success, "duration": duration})
    if not success:
        print("Workflow terminated early due to 'Integration Tests' failure.")
        return False, workflow_results

    workflow_end = time.time()
    total_workflow_duration = round(workflow_end - workflow_start, 3)
    print(json.dumps({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(workflow_end)),
        "workflow_status": "COMPLETED_SUCCESSFULLY",
        "total_duration_seconds": total_workflow_duration
    }))
    print("--- Workflow Simulation Finished ---")
    return True, workflow_results

if __name__ == "__main__":
    # The goal is to produce structured logs that can be analyzed to understand
    # step durations, failure rates, and identify bottlenecks or flaky steps.
    print("Simulating a workflow run to generate structured logs for observability.")
    print("Each line represents a JSON log entry from a workflow step.")
    simulate_github_workflow()
