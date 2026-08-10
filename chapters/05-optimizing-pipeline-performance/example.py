import time
import functools

class BuildSystem:
    def __init__(self):
        self.cache = {}
        self.max_concurrent_jobs = 3  # Simulates concurrency limit
        self.running_jobs = 0

    def _simulate_work(self, task_name, duration):
        """Simulates a task taking time."""
        print(f"  Starting '{task_name}'...")
        time.sleep(duration)
        print(f"  Finished '{task_name}'.")
        return f"Output of {task_name}"

    def build_step(self, step_name, dependencies, duration, use_cache=True):
        """
        A build step that can use a cache and respects concurrency limits.
        """
        cache_key = f"{step_name}-{'_'.join(dependencies)}"

        if use_cache and cache_key in self.cache:
            print(f"Cache hit for '{step_name}'. Using cached result.")
            return self.cache[cache_key]

        # Simulate concurrency control
        while self.running_jobs >= self.max_concurrent_jobs:
            print(f"  Concurrency limit reached. Waiting for a free slot...")
            time.sleep(0.5) # Wait for a job to finish

        self.running_jobs += 1
        try:
            print(f"Executing '{step_name}' (Dependencies: {dependencies})...")
            result = self._simulate_work(step_name, duration)
            if use_cache:
                self.cache[cache_key] = result
            return result
        finally:
            self.running_jobs -= 1

    def run_pipeline(self, steps_config, concurrency_enabled=True, cache_enabled=True):
        """Runs a simplified CI/CD pipeline."""
        print("\n--- Running Pipeline ---")
        self.cache.clear() # Clear cache for a fresh run
        self.running_jobs = 0

        step_results = {}
        for step_name, config in steps_config.items():
            deps = config.get('depends_on', [])
            duration = config.get('duration', 1)

            # Pass cache and concurrency flags to the build step
            result = self.build_step(
                step_name=step_name,
                dependencies=deps,
                duration=duration,
                use_cache=cache_enabled
            )
            step_results[step_name] = result
            print(f"Step '{step_name}' completed with result: {result}")
        print("--- Pipeline Finished ---\n")
        return step_results

# Define pipeline steps
pipeline_steps = {
    'install_deps': {'duration': 2, 'depends_on': []},
    'lint_code': {'duration': 1, 'depends_on': ['install_deps']},
    'run_tests': {'duration': 3, 'depends_on': ['install_deps']},
    'build_artifact': {'duration': 4, 'depends_on': ['run_tests', 'lint_code']},
    'deploy_to_dev': {'duration': 2, 'depends_on': ['build_artifact']}
}

build_system = BuildSystem()

print("--- First Run (No Cache, Concurrency Enabled) ---")
start_time = time.time()
build_system.run_pipeline(pipeline_steps, concurrency_enabled=True, cache_enabled=False)
end_time = time.time()
print(f"First run took: {end_time - start_time:.2f} seconds")

print("\n--- Second Run (Cache Enabled, Concurrency Enabled) ---")
# Simulate a change that doesn't affect 'install_deps' or 'lint_code' cache keys
# For simplicity, we just re-run with cache enabled.
start_time = time.time()
build_system.run_pipeline(pipeline_steps, concurrency_enabled=True, cache_enabled=True)
end_time = time.time()
print(f"Second run (with cache) took: {end_time - start_time:.2f} seconds")

print("\n--- Third Run (Cache Enabled, Concurrency Disabled - for comparison) ---")
# Reset cache to see impact of concurrency
build_system.cache.clear()
build_system.max_concurrent_jobs = 1 # Effectively disable concurrency
start_time = time.time()
build_system.run_pipeline(pipeline_steps, concurrency_enabled=False, cache_enabled=True)
end_time = time.time()
print(f"Third run (no concurrency, with cache) took: {end_time - start_time:.2f} seconds")
