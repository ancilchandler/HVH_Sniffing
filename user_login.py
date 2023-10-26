import argparse
import subprocess
import time

def login_with_curl(username, password, url):
    # Construct the curl command
    cmd = [
        'curl',
        '-X', 'POST',
        '-d', f'username={username}&password={password}',
        url
    ]
    
    # Execute the curl command
    response = subprocess.run(cmd, capture_output=True, text=True)
    return response.stdout

if __name__ == "__main__":
    # Hardcoded credentials
    users = {"admin": "SuperSeCurePassphrase999"}

    parser = argparse.ArgumentParser(description="Login to Flask server using curl")
    parser.add_argument("url", type=str, help="Full URL of the Flask server (e.g., http://192.168.92.130:8080)")

    args = parser.parse_args()

    LOGIN_URL = f'{args.url}/login'
    print(f"Targeting Flask server at: {LOGIN_URL}")

    while True:
        print("Attempting to log in with hardcoded credentials...")
        response = login_with_curl("admin", users["admin"], LOGIN_URL)
        print("Server Response:")
        print(response)  # Print the server response
        print("Waiting for 3 seconds before the next login attempt...")
        time.sleep(3)  # Wait for 3 seconds
