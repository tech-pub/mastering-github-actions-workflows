import time
import random
from datetime import datetime

# Simulate a complex build step with potential delays or failures
def simulate_build_step(step_name, min_duration=1, max_duration=5, success_rate=0.9):
    start_time = time.time()
    print(f"[{datetime.now().isoformat()}] INFO: Starting step '{step_name}'...")
    try:
        # Simulate work being done
        duration = random.uniform(min_duration, max_duration)
        time.sleep(duration)

        if random.random() > success_rate:
            raise RuntimeError(f"Simulated failure in step '{step_name}'")

        end_time = time.time()
        print(f"[{datetime.now().isoformat()}] INFO: Step '{step_name}' completed successfully in {end_time - start_time:.2f} seconds.")
        return True, end_time - start_time
    except Exception as e:
        end_time = time.time()
        print(f"[{datetime.now().isoformat()}] ERROR: Step '{step_name}' failed after {end_time - start_time:.2f} seconds. Error: {e}")
        return False, end_time - start_time

# Simulate an entire workflow run
def run_workflow():
    workflow_start_time = time.time()
    print(f"[{datetime.now().isoformat()}] INFO: Workflow started.")

    results = {}

    # Step 1: Checkout repository
    success, duration = simulate_build_step("Checkout Code", min_duration=0.5, max_duration=1.5)
    results["Checkout Code"] = {"success": success, "duration": duration}
    if not success:
        print(f"[{datetime.now().isoformat()}] CRITICAL: Workflow aborted due to failure in 'Checkout Code'.")
        return False, results

    # Step 2: Install dependencies
    success, duration = simulate_build_step("Install Dependencies", min_duration=2, max_duration=7, success_rate=0.8)
    results["Install Dependencies"] = {"success": success, "duration": duration}
    if not success:
        print(f"[{datetime.now().isoformat()}] CRITICAL: Workflow aborted due to failure in 'Install Dependencies'.")
        return False, results

    # Step 3: Run tests
    success, duration = simulate_build_step("Run Unit Tests", min_duration=3, max_duration=10, success_rate=0.95)
    results["Run Unit Tests"] = {"success": success, "duration": duration}
    if not success:
        print(f"[{datetime.now().isoformat()}] ERROR: 'Run Unit Tests' failed. Proceeding with caution.")
        # In a real scenario, this might abort or notify. Here we continue to show downstream impact.

    # Step 4: Build artifact
    success, duration = simulate_build_step("Build Artifact", min_duration=1.5, max_duration=6, success_rate=0.99)
    results["Build Artifact"] = {"success": success, "duration": duration}
    if not success:
        print(f"[{datetime.now().isoformat()}] CRITICAL: Workflow aborted due to failure in 'Build Artifact'.")
        return False, results

    workflow_end_time = time.time()
    total_workflow_duration = workflow_end_time - workflow_start_time
    print(f"[{datetime.now().isoformat()}] INFO: Workflow finished in {total_workflow_duration:.2f} seconds.")
    return True, results

if __name__ == "__main__":
    print("--- Starting Workflow Simulation ---")
    workflow_overall_success, step_results = run_workflow()

    print("\n--- Workflow Analysis ---")
    print(f"Workflow Status: {'SUCCESS' if workflow_overall_success else 'FAILURE'}")
    print("Step-by-step breakdown:")
    for step, data in step_results.items():
        status = "SUCCESS" if data["success"] else "FAILED"
        print(f"  - {step}: {status}, Duration: {data['duration']:.2f}s")
        if not data["success"]:
            print(f"    ACTION REQUIRED: Investigate '{step}' for bottlenecks or errors.")

    long_steps = {step: data['duration'] for step, data in step_results.items() if data['duration'] > 5}
    if long_steps:
        print("\nPotential Bottlenecks (steps over 5 seconds):")
        for step, duration in sorted(long_steps.items(), key=lambda item: item[1], reverse=True):
            print(f"  - {step}: {duration:.2f}s")
