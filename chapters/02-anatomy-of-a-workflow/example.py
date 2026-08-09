# A simple Python script to simulate a test suite.
# This script represents the 'steps' a GitHub Actions workflow would execute.

import os

def run_tests():
    """
    Simulates running a series of tests.
    In a real scenario, this would involve a test framework like pytest or unittest.
    """
    print("--- Starting Test Suite ---")

    # Simulate a few test cases
    test_results = []
    
    # Test case 1: Basic arithmetic
    try:
        assert 1 + 1 == 2
        print("Test 1: Addition passed.")
        test_results.append(True)
    except AssertionError:
        print("Test 1: Addition FAILED.")
        test_results.append(False)

    # Test case 2: String manipulation
    try:
        assert "hello".upper() == "HELLO"
        print("Test 2: String uppercase passed.")
        test_results.append(True)
    except AssertionError:
        print("Test 2: String uppercase FAILED.")
        test_results.append(False)

    # Test case 3: Simulate a potential failure
    try:
        # Let's say this test expects a specific environment variable
        # If not set, it might fail.
        if os.getenv("SHOULD_FAIL_TEST_3", "false").lower() == "true":
            assert False, "Simulated failure for Test 3"
        else:
            assert True
        print("Test 3: Conditional test passed.")
        test_results.append(True)
    except AssertionError as e:
        print(f"Test 3: Conditional test FAILED. {e}")
        test_results.append(False)


    print("--- Test Suite Finished ---")

    # Determine overall success or failure of the 'job'
    if all(test_results):
        print("All tests passed! Workflow step 'run_tests' was successful.")
        return 0  # Indicate success
    else:
        print("Some tests failed! Workflow step 'run_tests' encountered failures.")
        return 1  # Indicate failure

if __name__ == "__main__":
    # This block simulates the execution context of a GitHub Actions step.
    # The exit code determines the success or failure of the step.
    exit_code = run_tests()
    exit(exit_code)
