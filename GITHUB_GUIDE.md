# 📚 GitHub Project Management Guide

## ✅ Your Project is Already on GitHub!

**Repository URL**: https://github.com/Venkatkalyan21/fraud-shield

---

## 🔄 Daily Workflow - Keeping Project Synced

### 1. **Check Status** (See what changed)
```powershell
git status
```

### 2. **Add Changes** (Stage files)
```powershell
# Add all changes
git add .

# Or add specific files
git add filename.py
```

### 3. **Commit Changes** (Save with message)
```powershell
git commit -m "Description of what you changed"
```

### 4. **Push to GitHub** (Upload to cloud)
```powershell
git push origin main
```

---

## 📝 Common Commands

### View Changes
```powershell
# See what files changed
git status

# See detailed changes
git diff

# See commit history
git log --oneline
```

### Undo Changes
```powershell
# Undo changes to a file (before committing)
git checkout -- filename.py

# Unstage a file (after git add)
git reset HEAD filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

### Update from GitHub
```powershell
# Download latest changes from GitHub
git pull origin main
```

---

## 🎯 Best Practices

### 1. **Commit Frequently**
- Commit small, logical changes
- Use descriptive commit messages
- Example: `"Fix chart centering issue"` not `"fix"`

### 2. **Commit Messages Format**
```
Short description (50 chars max)

Longer explanation if needed
- What changed
- Why it changed
```

### 3. **Before Pushing**
1. Test your code locally
2. Check `git status`
3. Review changes with `git diff`
4. Commit with clear message
5. Push to GitHub

---

## 🔀 Working with Branches (Advanced)

### Create a New Branch
```powershell
# Create and switch to new branch
git checkout -b feature-name

# Or using newer syntax
git switch -c feature-name
```

### Switch Branches
```powershell
git checkout main
# or
git switch main
```

### Merge Branch
```powershell
git checkout main
git merge feature-name
```

---

## 📦 Sync Local with GitHub

### If GitHub has changes you don't have:
```powershell
# Pull latest from GitHub
git pull origin main
```

### If you have local changes:
```powershell
# 1. Add your changes
git add .

# 2. Commit
git commit -m "Your changes"

# 3. Pull (may need to merge)
git pull origin main

# 4. Push
git push origin main
```

---

## 🚨 Troubleshooting

### "Your branch is ahead"
```powershell
# Just push your changes
git push origin main
```

### "Your branch is behind"
```powershell
# Pull latest changes first
git pull origin main
# Then push
git push origin main
```

### "Merge conflict"
```powershell
# 1. Open conflicted files
# 2. Look for <<<<<< markers
# 3. Resolve conflicts manually
# 4. Add resolved files
git add .
# 5. Complete merge
git commit -m "Resolve merge conflicts"
```

### "Remote repository not found"
```powershell
# Re-add remote
git remote add origin https://github.com/Venkatkalyan21/fraud-shield.git

# Or update if exists
git remote set-url origin https://github.com/Venkatkalyan21/fraud-shield.git
```

---

## 📁 Project Structure on GitHub

Your project structure:
```
fraud-shield/
├── flask_app.py          # Main Flask app
├── utils.py              # Helper functions
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── Procfile              # Render deployment
├── render.yaml           # Render config
├── .gitignore           # Files to ignore
├── templates/           # HTML templates
│   ├── analyze.html
│   └── results.html
├── website/             # Static files
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── models/              # ML models (if included)
└── data/                # Data files (if included)
```

---

## 🔐 Security Tips

### Never Commit:
- `.env` files (environment variables)
- API keys or secrets
- Large model files (use Git LFS or exclude)
- Personal data files

### Already Protected:
- `.gitignore` prevents committing sensitive files
- Environment variables set in Render dashboard

---

## 📊 View Your Project on GitHub

1. Go to: https://github.com/Venkatkalyan21/fraud-shield
2. Browse files
3. View commit history
4. See deployment status (if connected)

---

## 🎓 Quick Reference Card

```powershell
# Daily workflow
git status              # Check changes
git add .              # Stage all
git commit -m "msg"    # Save
git push origin main   # Upload

# Update from GitHub
git pull origin main   # Download

# View history
git log --oneline      # See commits
```

---

## 💡 Pro Tips

1. **Always check `git status` before committing**
2. **Write clear commit messages**
3. **Pull before pushing if working with others**
4. **Use branches for experiments**
5. **Keep `.gitignore` updated**

---

## 🔗 Useful Links

- Your Repo: https://github.com/Venkatkalyan21/fraud-shield
- GitHub Docs: https://docs.github.com
- Git Tutorial: https://git-scm.com/docs

---

**Remember**: GitHub is your backup and collaboration tool. Push regularly! 🚀

