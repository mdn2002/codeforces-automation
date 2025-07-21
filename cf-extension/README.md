# Codeforces Problem Exporter Extension

## How to Use

1. Open Chrome and go to `chrome://extensions/`.
2. Enable "Developer mode" (top right).
3. Click "Load unpacked" and select this `cf-extension` folder.
4. Open a Codeforces problem in your browser.
5. Start the Python server in your project root:
   ```bash
   python3 cf_receiver.py
   ```
6. Press `Ctrl+Alt+C` while on the problem tab.
7. You should see an alert and the HTML will be sent to your Python script.

You can now parse the HTML in `last_problem.html` and automate your workflow! 