import os
import subprocess
import shutil

class GitHubActionsSimulator:
    """
    Simulates a GitHub Actions workflow runner to demonstrate action reuse.
    """

    def __init__(self, workspace_dir="simulated_workspace"):
        self.workspace_dir = workspace_dir
        os.makedirs(self.workspace_dir, exist_ok=True)
        print(f"Initialized GitHub Actions simulator in: {os.path.abspath(workspace_dir)}")

    def _run_command(self, command, cwd=None):
        """Helper to run shell commands and capture output."""
        try:
            result = subprocess.run(command, cwd=cwd or self.workspace_dir,
                                    check=True, shell=True,
                                    capture_output=True, text=True)
            print(f"  CMD Output (stdout):\n{result.stdout.strip()}")
            if result.stderr:
                print(f"  CMD Output (stderr):\n{result.stderr.strip()}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"  ERROR: Command failed with exit code {e.returncode}")
            print(f"  Stderr:\n{e.stderr}")
            print(f"  Stdout:\n{e.stdout}")
            raise

    def simulate_checkout_action(self, repo_url="https://github.com/octocat/Spoon-Knife"):
        """
        Simulates the 'actions/checkout' action to clone a repository.
        This represents reusing a common action.
        """
        print(f"\n--- Simulating 'actions/checkout' for {repo_url} ---")
        target_path = os.path.join(self.workspace_dir, "cloned_repo")
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
            print(f"  Removed existing '{target_path}'")

        print(f"  Cloning '{repo_url}' into '{target_path}'...")
        # In a real GitHub Action, this would be handled by the action itself.
        # Here, we simulate its effect.
        self._run_command(f"git clone {repo_url} {target_path}", cwd=self.workspace_dir)
        print(f"  Repository checked out. Contents:")
        self._run_command(f"ls -F {target_path}")
        return target_path

    def simulate_custom_action_step(self, script_content, name="Custom Script Step"):
        """
        Simulates a custom step that might be a simple script or part of a reusable action.
        """
        print(f"\n--- Simulating: {name} ---")
        script_path = os.path.join(self.workspace_dir, "temp_script.sh")
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755) # Make it executable

        print(f"  Running script:\n{script_content.strip()}")
        self._run_command(f"{script_path}", cwd=self.workspace_dir)
        os.remove(script_path)

    def cleanup(self):
        """Removes the simulated workspace."""
        if os.path.exists(self.workspace_dir):
            shutil.rmtree(self.workspace_dir)
            print(f"\nCleaned up workspace: {self.workspace_dir}")

# --- Demonstrate the simulation ---
if __name__ == "__main__":
    simulator = GitHubActionsSimulator()

    try:
        # Step 1: Reuse the 'actions/checkout' action (simulated)
        # This prevents us from writing 'git clone ...' ourselves in every workflow.
        repo_path = simulator.simulate_checkout_action()

        # Step 2: Use a simple custom script step (like a 'run' step in a workflow)
        # This is what we'd write if no action existed for a task.
        simulator.simulate_custom_action_step(
            "echo 'Hello from a custom script!'\nls -F",
            name="Manual Listing of Workspace"
        )

        # Step 3: Imagine a hypothetical 'actions/upload-artifact' (simulated)
        # Instead of writing 'tar -czf artifact.tar.gz ./dist && upload_to_s3 ...',
        # we'd just use a pre-built action. Here, we simulate its effect.
        print("\n--- Simulating 'actions/upload-artifact' ---")
        os.makedirs(os.path.join(repo_path, "build"), exist_ok=True)
        with open(os.path.join(repo_path, "build", "app.log"), "w") as f:
            f.write("Application build log content.")
        print(f"  Created a dummy artifact: {os.path.join(repo_path, 'build', 'app.log')}")
        print("  (In a real workflow, 'actions/upload-artifact' would now zip and upload this.)")

    except Exception as e:
        print(f"\nSimulation failed: {e}")
    finally:
        simulator.cleanup()
