import requests
import time
import urllib3
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Suppress SSL warnings since the server uses a self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://gifts.fireflyplus.com/wall-api"
CHANNEL = os.getenv("CHANNEL", "1032")
USER_ID = os.getenv("USER_ID")


def get_headers(token):
    return {
        "token": token,
        "Content-Type": "application/json",
    }


def get_common_body():
    return {
        "channel": CHANNEL,
        "countryCode": "BD",
        "device": "ios",
        "userId": USER_ID,
        "localTime": int(time.time() * 1000),
    }


def fetch_tasks(token):
    """Fetch the task list from the API using the provided token."""
    url = f"{BASE_URL}/wall/task/user"
    body = get_common_body()

    print("📡 Fetching task list...")
    headers = get_headers(token)
    try:
        resp = requests.post(url, headers=headers, json=body, verify=False)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != 0:
            print(f"❌ API returned error code: {data.get('code')}")
            return []

        tasks = data.get("data", [])
        print(f"✅ Found {len(tasks)} total tasks\n")
        return tasks
    except Exception as e:
        print(f"❌ Failed to fetch tasks: {e}")
        return []


def complete_task(token, task_id):
    """Send a completion request for a single task."""
    url = f"{BASE_URL}/wall/task/complete"
    body = {
        "channel": CHANNEL,
        "device": "ios",
        "userId": USER_ID,
        "taskId": task_id,
        "localTime": int(time.time() * 1000),
        "completionTime": 40746,
    }

    headers = get_headers(token)
    resp = requests.post(url, headers=headers, json=body, verify=False)
    resp.raise_for_status()
    return resp.json()


def main():
    print("--- Task Completer ---")

    if not USER_ID:
        print("❌ USER_ID not found in environment variables. Please check your .env file.")
        return
    
    # Prompt for token input directly
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        try:
            token = input("👉 Enter your token: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n🚫 Operation cancelled.")
            return

    if not token:
        print("❌ 'token' is required! Exiting.")
        return

    tasks = fetch_tasks(token)
    if not tasks:
        print("No tasks found.")
        return

    # Filter incomplete tasks with taskType == 1
    incomplete = []
    for t in tasks:
        # Filter logic: only taskType 1
        if t.get("taskType") != 1:
            continue

        remaining = t["taskCount"] - t["completeCount"]
        if remaining > 0:
            incomplete.append((t["taskId"], t["taskDetail"], remaining))

    if not incomplete:
        print("🎉 All taskType 1 tasks are already completed!")
        return

    print(f"📋 {len(incomplete)} incomplete taskType 1 task(s):\n")
    for tid, detail, remaining in incomplete:
        print(f"  • [{tid}] {detail.strip()} — {remaining} remaining")
    print()

    total_requests = sum(r for _, _, r in incomplete)
    done = 0

    for task_id, detail, remaining in incomplete:
        print(f"▶ Starting task [{task_id}]: {detail.strip()} ({remaining}x)")
        for i in range(remaining):
            done += 1
            try:
                result = complete_task(token, task_id)
                code = result.get("code", "?")
                print(f"   [{done}/{total_requests}] Task {task_id} attempt {i+1}/{remaining} → code: {code}")
            except Exception as e:
                print(f"   [{done}/{total_requests}] Task {task_id} attempt {i+1}/{remaining} → ERROR: {e}")

            if done < total_requests:
                time.sleep(1)

    print(f"\n🏁 Done! Sent {total_requests} completion request(s).")


if __name__ == "__main__":
    main()
