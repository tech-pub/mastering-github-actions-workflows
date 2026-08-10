# This example simulates a secure environment for a Python application
# demonstrating the use of 'secrets' (represented by environment variables)
# and 'environments' (represented by different function calls).

import os

# --- Simulate GitHub Secrets Management ---
# In a real GitHub Actions workflow, these would be securely fetched
# via `secrets.MY_API_KEY` or `secrets.DATABASE_PASSWORD`.
# For this local simulation, we use environment variables.

def set_mock_secrets(api_key, db_password):
    """Sets mock environment variables to simulate GitHub Secrets."""
    os.environ['MY_API_KEY'] = api_key
    os.environ['DATABASE_PASSWORD'] = db_password
    print("Mock secrets loaded.")

def get_secret(name):
    """Retrieves a 'secret' (environment variable)."""
    secret_value = os.environ.get(name)
    if secret_value:
        return secret_value
    else:
        raise ValueError(f"Secret '{name}' not found. "
                         "Ensure it's configured in your GitHub Secrets.")

# --- Simulate GitHub Environments ---
# Different 'environments' (e.g., staging, production) often have
# different secret values and configurations.

def deploy_to_staging():
    """Simulates deployment to the 'staging' environment."""
    print("\n--- Deploying to Staging Environment ---")
    try:
        api_key = get_secret('MY_API_KEY')
        db_password = get_secret('DATABASE_PASSWORD')

        # In a real application, these would be used to connect to
        # staging resources.
        print(f"Staging API Key: {api_key[:4]}...{api_key[-4:]}") # Masking for display
        print(f"Staging DB Password: {db_password[:2]}...{db_password[-2:]}") # Masking for display
        print("Staging deployment logic executed successfully.")
    except ValueError as e:
        print(f"Staging deployment failed: {e}")

def deploy_to_production():
    """Simulates deployment to the 'production' environment."""
    print("\n--- Deploying to Production Environment ---")
    try:
        api_key = get_secret('MY_API_KEY')
        db_password = get_secret('DATABASE_PASSWORD')

        # In a real application, these would be used to connect to
        # production resources.
        print(f"Production API Key: {api_key[:4]}...{api_key[-4:]}") # Masking for display
        print(f"Production DB Password: {db_password[:2]}...{db_password[-2:]}") # Masking for display
        print("Production deployment logic executed successfully.")
    except ValueError as e:
        print(f"Production deployment failed: {e}")

# --- Main execution flow ---
if __name__ == "__main__":
    # --- Step 1: Configure secrets for Staging and Production ---
    # In a real GitHub workflow, you would define these secrets
    # directly in GitHub's repository or organization settings,
    # and in environment-specific secrets.
    set_mock_secrets(
        api_key="sk_test_12345_staging",
        db_password="staging_db_secret_pass"
    )

    # --- Step 2: Run deployment to different environments ---
    # This demonstrates that the same code can use environment-specific
    # secrets based on the triggered workflow or environment.
    deploy_to_staging()

    # --- Simulate different secrets for Production (e.g., via environment-specific secrets) ---
    print("\n--- Simulating loading production secrets ---")
    set_mock_secrets(
        api_key="sk_live_abcde_production",
        db_password="production_db_super_secret_pass"
    )
    deploy_to_production()

    # Clean up mock environment variables
    del os.environ['MY_API_KEY']
    del os.environ['DATABASE_PASSWORD']
    print("\nMock secrets cleared.")
