# This Python script simulates a GitHub Actions workflow's expression evaluation.
# It demonstrates how context data can be used with expressions to create dynamic logic.

# --- Simulate GitHub Actions Contexts ---
# In a real GitHub Action, these would be automatically provided.
# Here, we define them as Python dictionaries for demonstration.

github_context = {
    "event": {
        "pull_request": {
            "head": {
                "ref": "feature/new-api-endpoint"
            },
            "base": {
                "ref": "main"
            }
        },
        "repository": {
            "name": "my-awesome-app"
        },
        "commits": [
            {"message": "feat: Add user authentication"},
            {"message": "fix: Correct database migration"}
        ]
    },
    "ref": "refs/heads/feature/new-api-endpoint",
    "sha": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
    "workflow": "CI/CD Pipeline"
}

env_context = {
    "NODE_VERSION": "16",
    "DEPLOY_ENVIRONMENT": "staging"
}

# Simulate outputs from a previous job/step
# In a real workflow, this would be `needs.<job_id>.outputs.<output_name>`
outputs_context = {
    "build_job": {
        "status": "success",
        "version": "1.0.0-beta"
    }
}

# --- Expression Evaluation Function ---
# This function mimics how GitHub Actions evaluates expressions.
# For simplicity, it uses basic string matching and dictionary lookups.
# A real expression engine is far more complex (e.g., handling operators, functions).

def evaluate_expression(expression: str, contexts: dict) -> bool:
    """
    Evaluates a simplified GitHub Actions-like expression against provided contexts.
    Supports basic `github.ref`, `github.event.pull_request.head.ref`, `env.<VAR>`,
    `outputs.<job_id>.<output_name>`, `contains`, and `startsWith`.
    """
    if "github.ref == 'refs/heads/main'" in expression:
        return contexts["github"]["ref"] == "refs/heads/main"
    elif "github.event.pull_request.head.ref == 'feature/new-api-endpoint'" in expression:
        return contexts["github"]["event"]["pull_request"]["head"]["ref"] == "feature/new-api-endpoint"
    elif "env.DEPLOY_ENVIRONMENT == 'production'" in expression:
        return contexts["env"]["DEPLOY_ENVIRONMENT"] == "production"
    elif "outputs.build_job.status == 'success'" in expression:
        return contexts["outputs"]["build_job"]["status"] == "success"
    elif "contains(github.event.commits[0].message, 'feat:')" in expression:
        return "feat:" in contexts["github"]["event"]["commits"][0]["message"]
    elif "startsWith(github.ref, 'refs/heads/feature/')" in expression:
        return contexts["github"]["ref"].startswith("refs/heads/feature/")
    return False # Default for unmatched expressions

# --- Workflow Logic Using Expressions ---

print("--- Simulating Workflow Logic ---")

# Example 1: Conditional job based on branch name
if evaluate_expression("github.ref == 'refs/heads/main'", {"github": github_context}):
    print("Action: Deploy to Production (triggered by push to main branch).")
else:
    print("Action: Not deploying to Production (not on main branch).")

# Example 2: Step conditional on pull request branch
if evaluate_expression("github.event.pull_request.head.ref == 'feature/new-api-endpoint'", {"github": github_context}):
    print("Action: Run API integration tests (feature branch specific).")
else:
    print("Action: Skipping API integration tests (not a specific feature branch).")

# Example 3: Step conditional on environment variable
if evaluate_expression("env.DEPLOY_ENVIRONMENT == 'production'", {"env": env_context}):
    print("Action: Running production-specific build steps.")
else:
    print("Action: Running development/staging build steps.")

# Example 4: Job conditional on previous job's output
if evaluate_expression("outputs.build_job.status == 'success'", {"outputs": outputs_context}):
    print("Action: Proceeding to deployment phase (previous build was successful).")
else:
    print("Action: Halting workflow (previous build failed).")

# Example 5: Conditional based on commit message content
if evaluate_expression("contains(github.event.commits[0].message, 'feat:')", {"github": github_context}):
    print("Action: Detected a 'feat:' commit, running new feature checks.")
else:
    print("Action: No 'feat:' commit detected, skipping new feature checks.")

# Example 6: Dynamic environment selection based on branch prefix
# In a real workflow, this might be used to set an 'environment' variable
branch_prefix_staging = evaluate_expression("startsWith(github.ref, 'refs/heads/feature/')", {"github": github_context})
branch_prefix_dev = evaluate_expression("startsWith(github.ref, 'refs/heads/develop/')", {"github": github_context})

if branch_prefix_staging:
    print(f"Detected feature branch: {github_context['ref']}. Setting target environment to 'staging'.")
elif branch_prefix_dev:
    print(f"Detected develop branch: {github_context['ref']}. Setting target environment to 'development'.")
else:
    print(f"Defaulting environment based on branch: {github_context['ref']}.")
