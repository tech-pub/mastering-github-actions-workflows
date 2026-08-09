import os

# --- Simulate a simplified "manual deployment" process ---
def manual_deployment(app_version: str, target_environment: str):
    """
    Simulates a manual deployment process.
    Highlights inconsistencies and potential errors.
    """
    print(f"--- Starting Manual Deployment for App v{app_version} to {target_environment} ---")
    
    # Junior engineers often make mistakes or forget steps
    if target_environment == "production":
        print("WARNING: Double-checking production deployment steps manually...")
        user_input = input("Are you sure you want to deploy to PROD? (yes/no): ").lower()
        if user_input != "yes":
            print("Manual deployment to production aborted.")
            return False

    # Simulate configuration file updates
    config_file = f"config_{target_environment}.txt"
    try:
        with open(config_file, "w") as f:
            f.write(f"APP_VERSION={app_version}\n")
            f.write(f"DATABASE_URL=manual_db_{target_environment}\n")
            # Junior engineer might forget to update a critical setting
            if target_environment == "staging":
                f.write("DEBUG_MODE=True # Forgot to disable for production!\n") 
            else:
                f.write("DEBUG_MODE=False\n")
        print(f"  - Updated {config_file} manually.")
        print(f"  - Deployed app version {app_version}.")
    except IOError as e:
        print(f"  - Error updating config file: {e}")
        return False

    # Simulate server restart - could fail if dependencies are missing
    print("  - Restarting server (manual step, prone to errors)...")
    # Imagine this fails intermittently due to manual setup differences
    if target_environment == "production" and app_version == "1.1":
        print("  - ERROR: Production server restart failed due to missing dependency (forgot to install manually)!")
        return False
        
    print(f"--- Manual Deployment to {target_environment} finished. ---")
    return True

# --- Illustrate the need for Infrastructure as Code (IaC) / Automation ---
# In a real CI/CD pipeline (like GitHub Actions), these steps would be automated.

def automated_deployment_step(step_name: str, success: bool = True):
    """Simulates a single step in an automated CI/CD pipeline."""
    if success:
        print(f"[✅ CI/CD] Executing: {step_name}")
    else:
        print(f"[❌ CI/CD] Failed: {step_name}")
        # In a real pipeline, this would stop the workflow

def ci_cd_pipeline(app_version: str, target_environment: str):
    """
    Simulates a CI/CD pipeline using 'Infrastructure as Code' principles.
    Each step is explicitly defined and automated, ensuring consistency.
    """
    print(f"\n--- Starting CI/CD Pipeline for App v{app_version} to {target_environment} ---")

    automated_deployment_step("Checkout code")
    automated_deployment_step("Install dependencies")
    automated_deployment_step("Run unit tests") # Ensures code quality
    automated_deployment_step("Build artifacts")

    # Configuration is defined as code, ensuring consistency across environments
    automated_deployment_step(f"Prepare configuration for {target_environment} (IaC)")
    
    # Deployment is automated and idempotent
    automated_deployment_step(f"Deploy app v{app_version} to {target_environment} (Automated)")
    automated_deployment_step(f"Run integration tests on {target_environment}") # Verifies deployment

    print(f"--- CI/CD Pipeline to {target_environment} finished. ---")


if __name__ == "__main__":
    print("Scenario 1: Manual Deployments - Prone to errors and inconsistencies.")
    manual_deployment("1.0", "staging")
    manual_deployment("1.0", "production") # Will prompt for confirmation
    manual_deployment("1.1", "production") # Simulates a production failure

    print("\n" + "="*80 + "\n")

    print("Scenario 2: CI/CD Pipeline - Consistent, repeatable, and less error-prone.")
    ci_cd_pipeline("1.0", "staging")
    ci_cd_pipeline("1.1", "production")

    # Clean up simulated config files
    for env in ["staging", "production"]:
        if os.path.exists(f"config_{env}.txt"):
            os.remove(f"config_{env}.txt")
