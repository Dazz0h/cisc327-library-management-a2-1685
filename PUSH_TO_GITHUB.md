# Push to GitHub Instructions

## Step 1: Create Repository on GitHub
1. Go to: https://github.com/new
2. Repository name: `cisc327-library-assignment4` (or your choice)
3. Visibility: **Public** ✅
4. Do NOT initialize with README
5. Click "Create repository"

## Step 2: Push Your Code

Replace `YOUR_USERNAME` with your GitHub username:

```bash
cd "c:\Users\lanke\Desktop\cisc327-library-management-a2-1685-main"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/cisc327-library-assignment4.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

## Example:
If your username is `emmanuelsmith`:
```bash
git remote add origin https://github.com/emmanuelsmith/cisc327-library-assignment4.git
git branch -M main
git push -u origin main
```

## Verify
After pushing, visit:
https://github.com/YOUR_USERNAME/cisc327-library-assignment4

You should see all your files!

## Need to Make Changes Later?

After making changes:
```bash
git add .
git commit -m "Update: description of changes"
git push
```
