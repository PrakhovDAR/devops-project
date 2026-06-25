import requests
import sys
import os

TARGET_URL = os.environ.get('APP_URL', 'http://app:5000')

def run_test():
    try:
        response = requests.get(TARGET_URL, timeout=5)
        print(f"Status code received: {response.status_code}")
        if response.status_code == 200:
            print("Integration test PASSED")
            sys.exit(0)
        else:
            print("Integration test FAILED", file=sys.stderr)
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_test()