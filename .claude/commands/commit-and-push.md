# Commit and Push Command

**Name:** `/commit-and-push`  
**Description:** Automated workflow to stage changes, generate commit message, get user approval, commit, and push to remote

## Workflow

1. **Stage all changes** - Add all modified files to git staging area
2. **Analyze changes** - Review git diff to understand what was changed
3. **Generate commit message** - Create a descriptive commit message following conventional commits format
4. **User review** - Present commit message to user for approval or editing
5. **Commit changes** - Create the git commit with the approved message
6. **Push to remote** - Push the committed changes to the remote repository

## Implementation

When this command is invoked:

1. Run `git add .` to stage all changes
2. Run `git status` and `git diff --staged` to analyze what's being committed
3. Generate a commit message based on:
   - File changes (added, modified, deleted)
   - Code patterns (features, fixes, refactoring, docs)
   - Security implications (if changes involve security modules)
   - Following conventional commits format: `type(scope): description`
4. Present the commit message to the user with options:
   -  Approve and commit
   -  Edit the message
   - L Cancel the operation
5. If approved, run `git commit -m "message"` (using standard commit format without AI attribution)
6. Push to remote with `git push`
7. Provide confirmation with commit hash and push status

## Commit Message Format

Generate standard commit messages following conventional commits format:

- `feat:` new features
- `fix:` bug fixes  
- `docs:` documentation changes
- `refactor:` code refactoring
- `security:` security-related changes
- `test:` adding or updating tests
- `chore:` maintenance tasks

Include scope when relevant (e.g., `feat(security): add CCPA compliance`)

**Important:** Commit messages should be standard and professional, without any AI-specific attribution or co-authoring tags. The commit should appear as if created by the repository owner. (Example: do not use something like docs(claude):)

## Safety Checks

- Verify we're in a git repository
- Check for uncommitted changes before staging
- Ensure we're not committing sensitive information
- Confirm remote branch exists before pushing
- Handle merge conflicts gracefully

## Error Handling

- If git operations fail, provide clear error messages
- If there are no changes to commit, inform the user
- If push fails due to remote changes, suggest pulling first
- Offer to retry operations if they fail