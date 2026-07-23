# Git Workflow

## Purpose

This document defines the Git workflow followed by the Supply Chain Analytics project to ensure smooth collaboration, version control, and code quality.

---

# Branch Structure

| Branch | Purpose |
|----------|---------|
| main | Stable production branch |
| main-clone | Integration and review branch |
| palak | Documentation, testing, and anomaly detection work |
| isaac | Forecasting module development |
| rajarshi | Data engineering and visualization |
| utsav | Backend architecture and project integration |

---

# Development Workflow

### Step 1: Update Local Repository

```bash
git checkout main-clone
git pull origin main-clone
```

---

### Step 2: Switch to Personal Branch

```bash
git checkout palak
```

---

### Step 3: Create or Modify Files

Implement assigned features or documentation.

Example:

- Documentation
- Testing
- Anomaly Detection
- API Validation

---

### Step 4: Check Status

```bash
git status
```

---

### Step 5: Stage Changes

```bash
git add .
```

or

```bash
git add docs/09_Git_Workflow.md
```

---

### Step 6: Commit Changes

```bash
git commit -m "Added Git Workflow documentation"
```

---

### Step 7: Push Personal Branch

```bash
git push origin palak
```

---

### Step 8: Merge into Integration Branch

```bash
git checkout main-clone
git merge palak
```

---

### Step 9: Push Integration Branch

```bash
git push origin main-clone
```

---

# Pre-Commit Validation

Before every commit the project automatically performs:

- Frontend Build
- Python Syntax Check
- Backend Formatting
- Ruff Lint
- Black Formatter
- isort Import Check
- Security Scan (Bandit if installed)

---

# Commit Message Guidelines

Use meaningful commit messages.

Examples:

```
Added PRD documentation
Added HLD documentation
Added LLD documentation
Added Development Guide
Added Testing Strategy
Fixed anomaly detection bug
Updated API schema
```

---

# Merge Strategy

1. Work only on your assigned branch.
2. Push changes to your branch.
3. Merge into **main-clone** after verification.
4. Resolve conflicts before pushing.
5. Never push incomplete work to the production branch.

---

# Best Practices

- Pull latest changes before starting work.
- Commit small logical changes.
- Write descriptive commit messages.
- Review changes before pushing.
- Keep the working tree clean.
- Resolve merge conflicts carefully.
- Test changes before merging.

---

# Common Git Commands

| Command | Description |
|----------|-------------|
| git status | Check repository status |
| git add . | Stage all changes |
| git commit -m "message" | Commit changes |
| git push origin palak | Push personal branch |
| git checkout main-clone | Switch branch |
| git pull origin main-clone | Get latest changes |
| git merge palak | Merge branch |
| git restore file | Discard local changes |
| git log --oneline | View commit history |

---

# Workflow Summary

```
Pull Latest Changes
        ↓
Checkout Personal Branch
        ↓
Develop / Update Files
        ↓
git status
        ↓
git add
        ↓
git commit
        ↓
git push origin <branch>
        ↓
Merge into main-clone
        ↓
Push main-clone
```

---

# Conclusion

Following this Git workflow ensures proper version control, clean collaboration, reliable code integration, and efficient project management throughout the development lifecycle.