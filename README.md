# Task Completer Script

This Python script automates the completion of specific tasks (Type 1) for the "Wearfit Pro" platform. It fetches the user's task list, filters for eligible tasks, and sends completion requests sequentially.

## ⚠️ Disclaimer
**For Educational Purposes Only.** usage of this script may violate the terms of service of the target platform. Use at your own risk.

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [Charles Proxy](https://www.charlesproxy.com/) (Trial version is sufficient)
- A mobile device (iOS/Android) connected to the same network as your PC running Charles.

## Setup

1.  **Clone/Download the code.**

2.  **Create and Activate Virtual Environment:**
    ```bash
    # Create virtual environment
    python3 -m venv venv

    # Activate it (Mac/Linux)
    source venv/bin/activate

    # Activate it (Windows)
    venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration:**
    - Rename `.env.example` to `.env`.
    - Open `.env` and set your `USER_ID` and `CHANNEL` (if different from default).
    ```bash
    cp .env.example .env
    # Edit .env with your actual values
    ```

## How to Get the Token (Walkthrough)

To use this script, you need a valid session `token`. We will use Charles Proxy to intercept the network traffic from your phone and fetch this token.

### Step 1: Configure Charles Proxy on PC
1.  Open **Charles Proxy**.
2.  Go to **Proxy > Proxy Settings**.
    - Check **Enable transparent HTTP proxying**.
    - Note the **Port** (usually `8888`).
3.  Go to **Proxy > SSL Proxying Settings**.
    - Check **Enable SSL Proxying**.
    - Click **Add** under "Includes".
    - Host: `gifts.fireflyplus.com`
    - Click **OK**.

### Step 2: Configure Mobile Device
1.  Make sure your phone and PC are on the **same Wi-Fi network**.
2.  Find your PC's local IP address (e.g., `192.168.1.x`).
3.  On your phone, go to **Wi-Fi Settings**.
4.  Tap the info icon (or modify network) for your connected Wi-Fi.
5.  Set **Configure Proxy** to **Manual**.
    - **Server**: Your PC's IP address.
    - **Port**: `8888` (or whatever you set in Charles).
6.  Save the settings.

### Step 3: Install SSL Certificate on Mobile
1.  Open Chrome/Safari on your phone.
2.  Go to `chls.pro/ssl`.
3.  It will prompt to download a configuration profile/certificate. Allow it.
4.  **For iOS:**
    - Go to **Settings > Profile Downloaded** and install the Charles Proxy certificate.
    - Go to **Settings > General > About > Certificate Trust Settings**.
    - Toggle **ON** full trust for the Charles Proxy certificate.
5.  **For Android:**
    - Follow system prompts to install the certificate (usually named "Charles Proxy").

### Step 4: Capture the Token
1.  Open the Wearfit Pro app on your phone.
2.  Navigate to the "Earn Gold Beans" or task section to trigger network requests.
3.  Check Charles on your PC. You should see requests to `gifts.fireflyplus.com`.
4.  Look for a request like:
    `GET/POST https://gifts.fireflyplus.com/wall-api/wall/task/user`
    OR
    `POST https://gifts.fireflyplus.com/wall-api/open/auth`
5.  Click on the request and check the **Contents** (Response) tab or the **Request Headers**.
6.  Find the `token` string (it's a long string usually starting with `eyJ...`).
7.  Copy this token.

## Usage

Run the script and paste the token when prompted:

```bash
# Activate virtual environment if not already active
source venv/bin/activate  # (Mac/Linux)
# venv\Scripts\activate   # (Windows)

python3 task_completer.py
```

Output:
```text
--- Task Completer ---
👉 Enter your token: <PASTE_TOKEN_HERE>
📡 Fetching task list...
✅ Found 15 total tasks

📋 5 incomplete taskType 1 task(s):
  • [1032U15] Visit 2 web pages... — 2 remaining
  ...

▶ Starting task [1032U15]...
   [1/5] Task 1032U15 attempt 1/2 → code: 0
   ...
🏁 Done!
```

## Troubleshooting

- **Script errors immediately:** Ensure you have created the `.env` file with a valid `USER_ID`.
- **"Certificate verify failed" errors:** The script suppresses these warnings, but ensure standard Python SSL libraries are up to date.
- **Charles not capturing traffic:** Ensure your firewall allows Charles, and your phone is strictly using the manual proxy to your PC's IP.
