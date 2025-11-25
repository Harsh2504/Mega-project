# 🚀 Quick Start Guide - Student Feedback System

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Setup](#quick-setup)
3. [First Time Login](#first-time-login)
4. [Testing the System](#testing-the-system)
5. [Common Issues](#common-issues)
6. [Development Workflow](#development-workflow)

---

## System Requirements

### Required Software
- **Python 3.7 or higher** - [Download](https://www.python.org/downloads/)
- **MySQL 8.0+** or **MySQL Workbench** - [Download](https://dev.mysql.com/downloads/)
- **Git** (optional) - [Download](https://git-scm.com/)
- **VS Code** (recommended) - [Download](https://code.visualstudio.com/)

### Check if Python is installed
```powershell
python --version
# Should show: Python 3.x.x
```

---

## Quick Setup

### Step 1: Database Setup

#### Option A: Using TiDB Cloud (Current Setup)
Your project is already configured for TiDB Cloud. No local MySQL needed!
```python
# Credentials in dbcon.py
Host: gateway01.us-west-2.prod.aws.tidbcloud.com
Port: 4000
Database: systemdb
```

#### Option B: Local MySQL Setup (Recommended for Development)
```powershell
# 1. Install XAMPP (includes MySQL)
# Download from: https://www.apachefriends.org/

# 2. Start MySQL from XAMPP Control Panel

# 3. Create database
# Open phpMyAdmin (http://localhost/phpmyadmin)
# Import systemdb.sql file
```

**Update `dbcon.py` for local MySQL:**
```python
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",  # Default XAMPP password is empty
        database="systemdb",
        connection_timeout=300
    )
    return connection
```

### Step 2: Python Environment Setup

```powershell
# Navigate to project folder
cd "C:\Users\HARSH\OneDrive\Desktop\Fillers\Mega-project"

# Create virtual environment
python -m venv env

# Activate virtual environment
.\env\Scripts\activate
# You should see (env) in your terminal

# Install dependencies
pip install -r requirements.txt

# If you get errors, install individually:
pip install Flask==2.2.2
pip install mysql-connector-python==8.0.32
pip install pandas==1.5.3
pip install openpyxl==3.1.1
pip install gunicorn==20.0.4
```

### Step 3: Run the Application

```powershell
# Make sure virtual environment is activated
# You should see (env) at the start of your terminal

# Run the app
python app.py

# You should see:
# * Running on http://127.0.0.1:8000
# * Debug mode: on
```

### Step 4: Access the Application

Open browser and go to:
```
http://localhost:8000
```

You should see the login page! 🎉

---

## First Time Login

### Admin Login
```
Email: naresh.kamble@sgipolytechnic.in
Password: 123456
```

### Sub-Admin Login (Electronics Dept)
```
Email: deepak.kamble@sgipolytechnic.in
Password: 9420584185
```

### What to Do After Login

1. **Admin Dashboard** - You'll see feedback scheduling options
2. **Sidebar Menu** - Click hamburger menu (☰) to see all options
3. **Check Department** - Go to "Department" to see all departments
4. **Check Faculty** - Go to "Faculty" to see all faculty members

---

## Testing the System

### Test 1: View Existing Data
```
1. Login as Admin
2. Sidebar → Department (see 6 departments)
3. Sidebar → Faculty (see faculty members)
4. Sidebar → Class (see FE, SE, TE)
5. Sidebar → Division (see divisions per class)
```

### Test 2: Add New Department
```
1. Go to Department page
2. Click "Add Department" button
3. Fill form:
   - Department Name: Test Department
   - Short Form: TD
4. Click Submit
5. Verify it appears in table
6. Delete it (click delete button)
```

### Test 3: Schedule Feedback
```
1. Go to Admin dashboard
2. Set Start Date/Time (future time)
3. Set End Date/Time (after start time)
4. Select Part (Part I or Part II)
5. Click "Start" button
6. Note the 6-digit code generated
7. Try clicking "Stop" to clear schedule
```

### Test 4: Student Feedback Flow
```
1. Schedule feedback (as admin)
2. Open new incognito window
3. Go to: http://localhost:8000/student_verify
4. Fill student details:
   - Department: Computer Science & Engineering
   - Class: Second Year (SE)
   - Division: (select one)
   - Batch: (select one)
   - Semester: 3 or 4
5. Enter 6-digit code
6. Click Submit
7. Answer feedback questions
8. Submit feedback
```

---

## Common Issues

### Issue 1: "Module not found" error
```powershell
# Make sure virtual environment is activated
.\env\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt
```

### Issue 2: Database connection error
```
Error: Can't connect to MySQL server

Solution 1: Check if MySQL is running
- XAMPP Control Panel → Start MySQL

Solution 2: Check credentials in dbcon.py
- Verify host, port, user, password

Solution 3: Test connection
python dbcon.py
# Should print department data if working
```

### Issue 3: Port 8000 already in use
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F

# Or change port in app.py (last line)
app.run(debug=True, port=8001)
```

### Issue 4: Templates not loading
```
Error: Template not found

Solution:
- Verify templates/ folder exists
- Check file names (case-sensitive)
- Restart Flask application
```

### Issue 5: Static files (CSS/JS) not loading
```
Solution:
1. Clear browser cache (Ctrl + Shift + Delete)
2. Hard refresh (Ctrl + F5)
3. Check static/ folder structure
4. Restart Flask application
```

---

## Development Workflow

### Making Changes

1. **Edit Code**
   - Make changes to app.py or templates
   - Flask auto-reloads in debug mode
   - Refresh browser to see changes

2. **Database Changes**
   ```sql
   -- Add new column
   ALTER TABLE users ADD COLUMN last_login DATETIME;
   
   -- Update data
   UPDATE users SET status='active' WHERE id=1;
   ```

3. **Testing Changes**
   - Test each change immediately
   - Use browser dev tools (F12)
   - Check console for JavaScript errors
   - Check terminal for Python errors

### Git Workflow (If Using)

```powershell
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Fixed password hashing bug"

# Push to GitHub
git push origin main
```

### Before Making Changes

```powershell
# Always create backup
# Export database
# From phpMyAdmin: Export → SQL

# Or via command line:
mysqldump -u root -p systemdb > backup_$(date +%Y%m%d).sql
```

---

## Quick Reference

### Restart Application
```powershell
# Stop: Ctrl + C in terminal
# Start: python app.py
```

### View Logs
```powershell
# Terminal shows real-time logs
# Look for:
# - 200 = Success
# - 404 = Not found
# - 500 = Server error
```

### Database Quick Check
```powershell
# Run database test
python dbcon.py

# Should show department data if connection works
```

### Clear Session (Force Logout)
```
1. Browser → Developer Tools (F12)
2. Application tab
3. Cookies → localhost
4. Delete all cookies
5. Refresh page
```

---

## File Structure Quick Reference

```
Mega-project/
├── app.py                 # Main application (edit this)
├── dbcon.py              # Database connection
├── requirements.txt      # Dependencies
├── systemdb.sql          # Database dump
│
├── templates/            # HTML files (edit these)
│   ├── login.html
│   ├── admin.html
│   ├── feedback.html
│   └── ...
│
├── static/               # CSS, JS, Images
│   ├── css/
│   ├── js/
│   └── images/
│
└── db/                   # Database schema files
    ├── users.sql
    ├── department.sql
    └── ...
```

---

## Next Steps

### Priority Order for Fixes

1. **Read Full Analysis**
   - Open `PROJECT_ANALYSIS.md`
   - Understand system architecture

2. **Review Bugs**
   - Open `BUGS_AND_FIXES.md`
   - Start with CRITICAL issues

3. **Implement Fixes**
   - Password hashing (30 min)
   - Environment variables (20 min)
   - CSRF protection (15 min)

4. **Test Everything**
   - Test each fix individually
   - Document what you changed

5. **Prepare for Deployment**
   - Update README
   - Create user manual
   - Backup everything

---

## Useful Commands

### Python/Flask
```powershell
# Activate environment
.\env\Scripts\activate

# Deactivate environment
deactivate

# Install package
pip install package_name

# List installed packages
pip list

# Create requirements file
pip freeze > requirements.txt
```

### Git
```powershell
# Clone repository
git clone https://github.com/Harsh2504/Mega-project.git

# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature/password-hashing

# View changes
git diff
```

### MySQL
```sql
-- Show all tables
SHOW TABLES;

-- Describe table structure
DESCRIBE users;

-- Count records
SELECT COUNT(*) FROM feedbacknew;

-- View recent feedback
SELECT * FROM feedbacknew ORDER BY id DESC LIMIT 10;

-- Check feedback schedule
SELECT * FROM works WHERE work='feedback';
```

---

## Keyboard Shortcuts

### VS Code
- `Ctrl + P` - Quick file open
- `Ctrl + Shift + F` - Search in all files
- `Ctrl + /` - Toggle comment
- `F5` - Start debugging
- `Ctrl + ` ` - Toggle terminal

### Browser Dev Tools
- `F12` - Open developer tools
- `Ctrl + Shift + C` - Inspect element
- `Ctrl + Shift + J` - Console
- `Ctrl + Shift + R` - Hard refresh (clear cache)

---

## Getting Help

### Documentation
- Flask: https://flask.palletsprojects.com/
- MySQL: https://dev.mysql.com/doc/
- Bootstrap: https://getbootstrap.com/docs/4.6/

### When Stuck
1. Read error message carefully
2. Check terminal for Python errors
3. Check browser console for JS errors
4. Search error on Google/Stack Overflow
5. Check if database is running
6. Verify all files are saved
7. Restart application

### Error Examples
```python
# ImportError
# Solution: pip install missing-package

# TemplateNotFound
# Solution: Check templates/ folder, verify file name

# DatabaseError
# Solution: Check if MySQL is running, verify credentials

# AttributeError: 'NoneType'
# Solution: Database query returned nothing, check your WHERE clause
```

---

## Tips for College Submission

1. **Clean Code**
   - Remove commented code
   - Add helpful comments
   - Fix indentation

2. **Documentation**
   - Update README.md
   - Create user manual
   - Add screenshots

3. **Demo Preparation**
   - Test all features
   - Prepare sample data
   - Practice explaining code

4. **Backup Everything**
   - Database backup
   - Code backup
   - Screenshots backup

5. **Be Honest**
   - Acknowledge known issues
   - Explain design decisions
   - Show what you learned

---

## Success Checklist

- [ ] Python installed and working
- [ ] MySQL/XAMPP installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database imported
- [ ] Application running on localhost:8000
- [ ] Can login as admin
- [ ] Can view departments, faculty, etc.
- [ ] Can schedule feedback
- [ ] Can submit feedback as student
- [ ] Reviewed PROJECT_ANALYSIS.md
- [ ] Reviewed BUGS_AND_FIXES.md
- [ ] Ready to start making improvements

---

**You're all set! Start with reading the PROJECT_ANALYSIS.md file, then tackle the bugs one by one from BUGS_AND_FIXES.md** 🚀

Good luck with your project! Remember - it's already a solid system, you're just making it better! 💪

---

*Last Updated: November 24, 2025*
