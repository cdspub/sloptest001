# Development
Never add inline documentation.
Never add unit tests.
Never modify `.gitignore` file.
Never commit `__pycache__`.

You are working on the `main` branch that may have external changes. Run `git fetch` and `git pull --rebase origin main` before processing any of the user's requests. Inspect and understand the changes carefully.

`TODOS` is a special file with user instructions. Always check after pulling the repo for unfinished tasks and address them automatically.

Check for inline `BOT` comments in changed files after pulling the repo. Address them automatically.
