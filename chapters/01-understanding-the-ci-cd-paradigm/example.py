import os
import subprocess

def simulate_manual_deployment():
    """
    Simulates a manual deployment process with potential for human error.
    A junior engineer might accidentally deploy the wrong version or misconfigure.
    """
    print("--- Starting Manual Deployment Simulation ---")
    app_version = input("Enter application version to deploy (e.g., v1.0.0, v1.0.1): ")
    config_setting = input("Enter a critical configuration setting (e.g., 'production' or 'staging'): ")

    if not app_version.startswith("v"):
        print("ERROR: Manual deployment failed! Invalid version format. Must start with 'v'.")
        return False

    if config_setting not in ["production", "staging"]:
        print("ERROR: Manual deployment failed! Invalid configuration setting. Must be 'production' or 'staging'.")
        return False

    print(f"Manually deploying version: {app_version} with configuration: {config_setting}...")
    # Simulate deployment steps
    try:
        # Imagine copying files, running scripts, etc.
        subprocess.run(['echo', f'Deploying {app_version} to {config_setting} environment...'], check=True)
        print("Manual deployment successful (simulated).")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Manual deployment failed during execution: {e}")
        return False

def simulate_iac_deployment(app_version: str, config_setting: str):
    """
    Simulates an Infrastructure-as-Code (IaC) driven deployment.
    This process is automated and consistent, reducing human error.
    """
    print("\n--- Starting Infrastructure-as-Code (IaC) Deployment Simulation ---")
    print(f"Using IaC to deploy version: {app_version} with configuration: {config_setting}...")

    # In a real scenario, this would involve tools like Terraform, Ansible, etc.
    # We'll simulate by checking the parameters and confirming the deployment.
    if not app_version.startswith("v"):
        print("ERROR: IaC deployment failed! Invalid version format detected by IaC script.")
        return False

    if config_setting not in ["production", "staging"]:
        print("ERROR: IaC deployment failed! Invalid configuration setting detected by IaC script.")
        return False

    # Simulate IaC applying infrastructure and deploying the app
    try:
        # Imagine calling an IaC tool like 'terraform apply -var="app_version={app_version}"'
        subprocess.run(['echo', f'Executing IaC script for {app_version} to {config_setting} environment...'], check=True)
        print("IaC deployment successful (simulated). Consistency ensured.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"IaC deployment failed during execution: {e}")
        return False

if __name__ == "__main__":
    print("Scenario 1: Junior engineer attempts manual deployment (prone to error).")
    success_manual = simulate_manual_deployment()
    print(f"Manual deployment result: {'Success' if success_manual else 'Failure'}")

    print("\nScenario 2: Automated deployment via Infrastructure-as-Code (consistent and reliable).")
    # These parameters would come from a GitHub Actions workflow or a version control system.
    IAC_APP_VERSION = "v2.0.0"
    IAC_CONFIG = "production"
    success_iac = simulate_iac_deployment(IAC_APP_VERSION, IAC_CONFIG)
    print(f"IaC deployment result: {'Success' if success_iac else 'Failure'}")

    print("\n--- Summary ---")
    print("Manual deployments are risky due to human error and inconsistency.")
    print("Infrastructure-as-Code (IaC) provides automation and consistency,")
    print("making deployments reliable, which is a core tenet of CI/CD and GitHub Actions.")
