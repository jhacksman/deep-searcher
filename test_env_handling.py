import os
from demo import confirm_env_var

def test_env_vars():
    print("Testing environment variable confirmation:")
    
    # Test with existing env var
    print("\nTesting with existing env var:")
    os.environ["TEST_VAR"] = "test-value"
    result = confirm_env_var("TEST_VAR")
    print(f"Result: {result}")
    
    # Test with missing env var
    print("\nTesting with missing env var:")
    if "MISSING_VAR" in os.environ:
        del os.environ["MISSING_VAR"]
    result = confirm_env_var("MISSING_VAR", default="default-value")
    print(f"Result: {result}")

if __name__ == "__main__":
    test_env_vars()
