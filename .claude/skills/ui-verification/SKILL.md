---
name: ui-verification
description: Mandatory end-to-end verification procedure after adding or modifying any UI feature (buttons, modals, navigation flows) in this project's Flask app — start the real server on port 5002 (never 5001), click every new button, trace JS errors, verify navigation, prove each interaction with a screenshot/eval, then stop the server. Load whenever UI work needs verifying before it's considered done.
---

# UI Verification (MANDATORY)

After adding or modifying any UI feature — especially new buttons, modals, or navigation flows:

1. **Always start the real web server on port 5002** (`preview_start` with port 5002 — do NOT use 5001, that port belongs to the user's running instance).
2. **Click every new button** and verify it performs the correct action (use `preview_eval` to simulate clicks if needed).
3. **Trace JS errors**: use `preview_console_logs` and `preview_eval` to check for `undefined`, `null`, or scoping issues (e.g. variables declared inside an IIFE are not accessible outside it).
4. **Verify navigation flows end-to-end**: if a button should navigate to another view, confirm the target view actually appears.
5. Do not consider UI work done until you have a screenshot or eval result proving each new interaction works.
6. **Always stop the server (`preview_stop` + `lsof -ti :5002 | xargs kill -9`) the moment testing is finished.** Never leave a test server running.
