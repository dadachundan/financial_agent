# Workflow Instructions

After completing a task and verifying that it works (by running tests or the app):

1. Create a concise Git commit using Conventional Commits (e.g., `fix:`, `feat:`).
2. Push the changes to the `main` branch on GitHub.
3. Ensure the local `main` is synced with the remote `HEAD`.
4. Do not include the "Co-authored-by: Claude" footer in commits.

# Hotspot / Network Push Limitations

When working on a hotspot or restricted network, pushing directly to `main` may
fail with HTTP 403. In that case:

1. Push to the `claude/<branch-name>` feature branch instead (this always works).
2. Open a Pull Request on GitHub to merge the feature branch into `main`.
3. The PR link is printed by `git push` — share it with the user or open it manually.
4. After the PR is merged on GitHub, sync local `main`:
   ```bash
   git checkout main && git pull origin main
   ```
