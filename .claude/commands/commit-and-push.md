## commit-and-push

Automated workflow to stage changes, generate commit message, get user approval, commit, and push to remote

### Usage
```
/commit-and-push
```

### Description
This command automates the entire git workflow:
1. Stage all changes (`git add .`)
2. Analyze changes (`git status` and `git diff --staged`)
3. Generate a smart commit message following conventional commits format
4. Present the message to user for approval/editing
5. Commit the changes
6. Push to remote repository

### Workflow Steps
1. Run `git status` and `git diff` to analyze current changes
2. Run `git add .` to stage all changes  
3. Run `git diff --staged` to review what will be committed
4. Generate a commit message based on:
   - File changes (added, modified, deleted)
   - Code patterns (features, fixes, refactoring, docs)
   - Security implications (if changes involve security modules)
   - Following conventional commits format: `type(scope): description`
5. Present the commit message to the user with options to:
   - Approve and proceed with commit
   - Edit the message before committing
   - Cancel the operation
6. If approved, run `git commit -m "approved_message"`
7. Push to remote with `git push`
8. Provide confirmation with commit hash and push status

### Commit Message Format
- `feat:` new features
- `fix:` bug fixes  
- `docs:` documentation changes
- `refactor:` code refactoring
- `security:` security-related changes
- `test:` adding or updating tests
- `chore:` maintenance tasks

### Safety Features
- Verifies git repository status
- Checks for sensitive information before committing
- Handles merge conflicts gracefully
- Provides clear error messages and retry options