# actions/my-custom-action/action.yml
# This file defines a GitHub Action using JavaScript.
# name: 'My Custom Action'
# description: 'Performs a standardized internal check and reports.'
# inputs:
#   project-name:
#     description: 'The name of the project being checked.'
#     required: true
# outputs:
#   status:
#     description: 'The status of the internal check (success or failure).'
# runs:
#   using: 'node16'
#   main: 'index.js'


# actions/my-custom-action/index.js
# This is the JavaScript code for the custom action.
# const core = require('@actions/core');
# const github = require('@actions/github');

# try {
#   const projectName = core.getInput('project-name');
#   console.log(`Performing internal check for project: ${projectName}`);

#   // Simulate a complex internal check based on company standards
#   // In a real scenario, this might involve API calls,
#   # database queries, or specific file validations.
#   const isStandardCompliant = projectName.startsWith('ORG-') && projectName.length > 5;

#   if (isStandardCompliant) {
#     core.setOutput('status', 'success');
#     console.log(`Project '${projectName}' is compliant with organizational standards.`);
#   } else {
#     core.setFailed(`Project '${projectName}' does not meet organizational standards.`);
#     core.setOutput('status', 'failure');
#   }
# } catch (error) {
#   core.setFailed(error.message);
# }


# .github/workflows/standardized-build.yml
# This file demonstrates how to use the custom action in a workflow.
# name: Standardized Build Check

# on:
#   push:
#     branches:
#       - main

# jobs:
#   build-and-check:
#     runs-on: ubuntu-latest
#     steps:
#     - name: Checkout repository
#       uses: actions/checkout@v3

#     - name: Run internal compliance check
#       uses: ./actions/my-custom-action
#       id: compliance_check
#       with:
#         project-name: 'ORG-WebApp' # Example of a compliant project name

#     - name: Report check status
#       run: |
#         echo "Compliance check result: ${{ steps.compliance_check.outputs.status }}"
#         if [ "${{ steps.compliance_check.outputs.status }}" == "failure" ]; then
#           echo "Build failed due to non-compliant project name."
#           exit 1
#         fi

#     - name: Run internal compliance check (non-compliant example)
#       uses: ./actions/my-custom-action
#       id: non_compliant_check
#       with:
#         project-name: 'WebApp' # Example of a non-compliant project name

#     - name: Report non-compliant check status
#       run: |
#         echo "Non-compliant check result: ${{ steps.non_compliant_check.outputs.status }}"
#         if [ "${{ steps.non_compliant_check.outputs.status }}" == "failure" ]; then
#           echo "Expected failure for non-compliant project name."
#         fi
