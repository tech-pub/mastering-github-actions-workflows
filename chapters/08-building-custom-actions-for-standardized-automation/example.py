# python_action.py

import os
import json
import requests

def run_custom_security_scan(repo_url, branch_name, severity_threshold='HIGH'):
    """
    Simulates a custom security scan action tailored for an organization.
    This example uses a dummy API call and predefined vulnerabilities.

    In a real scenario, this would integrate with internal security tools,
    proprietary scanners, or custom rule engines.
    """
    print(f"--- Running Custom Security Scan for '{repo_url}' on branch '{branch_name}' ---")

    # Simulate fetching custom security rules or configurations from an internal system
    # In a real action, this might be a call to an internal API or a configuration file.
    try:
        # Dummy API call simulation - replace with actual internal service discovery/call
        response = requests.get('https://api.example.com/internal/security-rules', timeout=5)
        response.raise_for_status()
        internal_security_config = response.json()
        print(f"Loaded internal security config: {internal_security_config.get('rules_version', 'N/A')}")
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        print("Could not connect to internal security rules API. Using default rules.")
        internal_security_config = {"rules_version": "1.0", "custom_checks": ["SQL_INJECTION_PATTERN", "HARDCODED_CREDENTIALS"]}


    # Simulate scan results based on custom organizational rules
    found_vulnerabilities = []
    if "SQL_INJECTION_PATTERN" in internal_security_config.get("custom_checks", []):
        if "sensitive_query" in repo_url: # Dummy logic
            found_vulnerabilities.append({"type": "SQL Injection", "severity": "CRITICAL", "file": "src/data.py"})
    if "HARDCODED_CREDENTIALS" in internal_security_config.get("custom_checks", []):
        if "config.py" in repo_url: # Dummy logic
            found_vulnerabilities.append({"type": "Hardcoded Credentials", "severity": "HIGH", "file": "src/config.py"})

    # Evaluate against the provided severity threshold
    action_successful = True
    critical_issues_found = False
    for vuln in found_vulnerabilities:
        print(f"  - Found: {vuln['type']} (Severity: {vuln['severity']}) in {vuln['file']}")
        if vuln['severity'] == 'CRITICAL':
            critical_issues_found = True
        if severity_threshold in ['CRITICAL', 'HIGH'] and vuln['severity'] in ['CRITICAL', 'HIGH']:
            action_successful = False
        elif severity_threshold == 'MEDIUM' and vuln['severity'] in ['CRITICAL', 'HIGH', 'MEDIUM']:
            action_successful = False

    if not found_vulnerabilities:
        print("  No custom security vulnerabilities detected.")
    else:
        print(f"--- Scan finished. Total vulnerabilities: {len(found_vulnerabilities)} ---")

    # Set GitHub Actions output
    # In a real GitHub Action, these would be echoed to stdout in a specific format
    # print(f"::set-output name=scan_successful::{'true' if action_successful else 'false'}")
    # print(f"::set-output name=critical_issues_found::{'true' if critical_issues_found else 'false'}")
    # print(f"::set-output name=vulnerabilities_json::{json.dumps(found_vulnerabilities)}")

    # For demonstration, we'll just print them.
    print(f"\n[Action Output Simulation]")
    print(f"scan_successful: {'true' if action_successful else 'false'}")
    print(f"critical_issues_found: {'true' if critical_issues_found else 'false'}")
    print(f"vulnerabilities_json: {json.dumps(found_vulnerabilities, indent=2)}")

    if not action_successful:
        print("\n::error::Custom security scan failed due to high-severity vulnerabilities.")
        # In a real GitHub Action, os.exit(1) would fail the workflow.
        # exit(1)
    else:
        print("\nCustom security scan passed.")

if __name__ == "__main__":
    # Simulate GitHub Action inputs from environment variables
    # In a real GitHub Action, inputs are passed as environment variables prefixed with INPUT_
    # For example, INPUT_REPO_URL, INPUT_BRANCH, INPUT_SEVERITY_THRESHOLD
    repo_url = os.getenv('INPUT_REPO_URL', 'https://github.com/my-org/my-sensitive-query-project')
    branch_name = os.getenv('INPUT_BRANCH', 'main')
    severity_threshold = os.getenv('INPUT_SEVERITY_THRESHOLD', 'HIGH')

    run_custom_security_scan(repo_url, branch_name, severity_threshold)

    # Example 2: Simulating a different repository and config
    print("\n" + "="*80 + "\n")
    print("Simulating another scan with a different repository...")
    os.environ['INPUT_REPO_URL'] = 'https://github.com/my-org/my-other-project-config.py'
    os.environ['INPUT_SEVERITY_THRESHOLD'] = 'MEDIUM'
    repo_url_2 = os.getenv('INPUT_REPO_URL')
    severity_threshold_2 = os.getenv('INPUT_SEVERITY_THRESHOLD')
    run_custom_security_scan(repo_url_2, branch_name, severity_threshold_2)
