import os

# --- GitHub Actions Contexts (Simulated) ---
# In a real GitHub Actions workflow, these would be automatically provided.
# We're simulating them for a runnable Python example.

github_context = {
    "event": {
        "pull_request": {
            "head": {"ref": "feature/new-api-endpoint"},
            "base": {"ref": "main"},
            "merged": False,
        },
        "repository": {"default_branch": "main"},
    },
    "ref": "refs/heads/feature/new-api-endpoint",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
    "run_id": "123456789",
    "actor": "octocat",
}

job_context = {
    "status": "success",  # Can be 'success', 'failure', 'cancelled'
    "container": {"id": "abcdef12345"},
}

steps_context = {
    "checkout": {"outputs": {}},
    "build": {"outputs": {"build_id": "myapp-v1.0-123", "image_tag": "latest"}},
}

env_context = {
    "DEPLOY_ENV": "staging",
    "GREETING_MESSAGE": "Hello from workflow!",
}

# --- GitHub Actions Expression Language Simulation ---
# This function simulates the evaluation of GitHub Actions expressions.
# It's a simplified version focusing on common patterns like `startsWith`, `contains`, `==`, `!=`, and context access.
def evaluate_expression(expression: str, github: dict, job: dict, steps: dict, env: dict) -> bool:
    # Replace context references with their simulated values
    expression = expression.replace("github.", "github_context['")
    expression = expression.replace("job.", "job_context['")
    expression = expression.replace("steps.", "steps_context['")
    expression = expression.replace("env.", "env_context['")

    # Handle common functions (startsWith, contains)
    expression = expression.replace("startsWith(", "str(").replace("), ", ").startswith(str(")
    expression = expression.replace("contains(", "str(").replace("), ", ").find(str(") != -1")

    # Finalize context access for evaluation
    expression = expression.replace("']", "']")

    try:
        # Use eval to interpret the expression string as Python code
        # In a real scenario, this would be handled by GitHub's secure expression parser.
        # We're making a strong assumption about the expression's safety for this demo.
        return eval(expression, {"github_context": github, "job_context": job, "steps_context": steps, "env_context": env})
    except Exception as e:
        print(f"Error evaluating expression '{expression}': {e}")
        return False

# --- Workflow Logic using Expressions ---

print("--- Simulating Workflow Conditions ---")

# Condition 1: Run only on pull requests targeting 'main'
condition_pr_to_main = "github.event_name == 'pull_request' && github.event.pull_request.base.ref == 'main'"
if evaluate_expression(condition_pr_to_main, github_context, job_context, steps_context, env_context):
    print(f"Condition 'Deploy PR to Main': TRUE. Deploying pull request to main.")
else:
    print(f"Condition 'Deploy PR to Main': FALSE. Not a PR to main.")

# Condition 2: Deploy to staging if branch starts with 'feature/'
condition_deploy_staging = "startsWith(github.ref, 'refs/heads/feature/') && env.DEPLOY_ENV == 'staging'"
if evaluate_expression(condition_deploy_staging, github_context, job_context, steps_context, env_context):
    print(f"Condition 'Deploy Staging Feature Branch': TRUE. Deploying to staging.")
else:
    print(f"Condition 'Deploy Staging Feature Branch': FALSE. Not a feature branch or not staging env.")

# Condition 3: Only deploy to production if build step succeeded and image tag is 'latest'
condition_deploy_prod = "job.status == 'success' && steps.build.outputs.image_tag == 'latest' && env.DEPLOY_ENV == 'production'"
# Modify env_context to simulate production deployment for this check
env_context["DEPLOY_ENV"] = "production"
if evaluate_expression(condition_deploy_prod, github_context, job_context, steps_context, env_context):
    print(f"Condition 'Deploy Production': TRUE. Deploying {steps_context['build']['outputs']['build_id']} to production.")
else:
    print(f"Condition 'Deploy Production': FALSE. Build not ready or not production env.")
env_context["DEPLOY_ENV"] = "staging" # Reset for other checks

# Condition 4: Send a notification if workflow actor is 'octocat'
condition_notify_octocat = "github.actor == 'octocat'"
if evaluate_expression(condition_notify_octocat, github_context, job_context, steps_context, env_context):
    print(f"Condition 'Notify Octocat': TRUE. Sending notification to {github_context['actor']}.")
else:
    print(f"Condition 'Notify Octocat': FALSE. Not octocat.")

print(f"\nExample of accessing a specific output: Build ID is {steps_context['build']['outputs']['build_id']}")
print(f"Example of accessing an environment variable: Greeting is '{env_context['GREETING_MESSAGE']}'")
