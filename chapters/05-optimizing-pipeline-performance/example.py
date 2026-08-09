import time
import functools

class BuildSystem:
    def __init__(self):
        self.build_cache = {}
        self.active_builds = 0
        self.max_concurrent_builds = 2 # Simulate concurrency control

    def _simulate_work(self, task_name, duration):
        """Simulates a task taking time."""
        print(f"  Starting '{task_name}'...")
        time.sleep(duration)
        print(f"  Finished '{task_name}'.")

    def build_component(self, component_name, rebuild_needed=False):
        """
        Simulates building a software component.
        Uses caching to avoid redundant work.
        """
        cache_key = f"build_{component_name}"
        if cache_key in self.build_cache and not rebuild_needed:
            print(f"Cache hit for '{component_name}'. Skipping build.")
            return True

        if self.active_builds >= self.max_concurrent_builds:
            print(f"Too many concurrent builds. Waiting for an available slot to build '{component_name}'.")
            while self.active_builds >= self.max_concurrent_builds:
                time.sleep(0.1) # Simulate waiting

        self.active_builds += 1
        print(f"Building '{component_name}' (no cache or rebuild requested)...")
        self._simulate_work(f"Compile {component_name}", 2)
        self._simulate_work(f"Test {component_name}", 1)
        self.build_cache[cache_key] = True  # Mark as built
        self.active_builds -= 1
        return True

def main():
    build_system = BuildSystem()

    print("--- Initial Pipeline Run (cold cache, sequential build for demo) ---")
    start_time = time.time()
    build_system.build_component("frontend_app")
    build_system.build_component("backend_service")
    build_system.build_component("database_migrations")
    print(f"Initial run took {time.time() - start_time:.2f} seconds.\n")

    print("--- Second Pipeline Run (hot cache, demonstrating cache hit) ---")
    start_time = time.time()
    build_system.build_component("frontend_app") # Should be cached
    build_system.build_component("backend_service", rebuild_needed=True) # Simulate a change, force rebuild
    build_system.build_component("database_migrations") # Should be cached
    print(f"Second run took {time.time() - start_time:.2f} seconds.\n")

    print("--- Third Pipeline Run (concurrency demonstration) ---")
    # Reset cache for a fresh concurrency demo
    build_system.build_cache = {}
    build_system.max_concurrent_builds = 2 # Set max concurrent builds

    start_time = time.time()
    # These will attempt to run concurrently
    build_system.build_component("module_A")
    build_system.build_component("module_B")
    build_system.build_component("module_C")
    print(f"Third run (with concurrency) took {time.time() - start_time:.2f} seconds.\n")

if __name__ == "__main__":
    main()
