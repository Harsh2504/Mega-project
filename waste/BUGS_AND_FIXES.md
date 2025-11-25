# 🐛 Bugs & Fixes Priority List

## 🚨 CRITICAL (Fix Before Deployment)

### 1. Password Security Issue
**Problem:** Passwords stored in plain text  
**File:** `app.py`, `dbcon.py`  
**Risk:** High - Anyone with database access can see all passwords

**Fix:**
```python
# Add to requirements.txt
# werkzeug (already included in Flask)

# In app.py - Update login route
from werkzeug.security import generate_password_hash, check_password_hash

# When creating user (add_user route)
hashed_password = generate_password_hash(password, method='sha256')

# When checking login
if user and check_password_hash(user[6], password):
    # Login successful
```

**Migration Script Needed:**
```python
# migrate_passwords.py
import mysql.connector
from werkzeug.security import generate_password_hash

mydb = mysql.connector.connect(...)
cursor = mydb.cursor()
cursor.execute("SELECT id, password FROM users")
users = cursor.fetchall()

for user in users:
    user_id, plain_password = user
    hashed = generate_password_hash(plain_password, method='sha256')
    cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed, user_id))
    
mydb.commit()
```

---

### 2. Secret Key Hardcoded
**Problem:** `app.secret_key = 'your_secret_key'`  
**File:** `app.py` line 10  
**Risk:** Medium - Session hijacking possible

**Fix:**
```python
# Install python-dotenv
pip install python-dotenv

# Create .env file (ADD TO .gitignore!)
SECRET_KEY=your-random-secret-key-here-min-32-chars
DB_HOST=gateway01.us-west-2.prod.aws.tidbcloud.com
DB_PORT=4000
DB_USER=3vBMzU5RHaXD1tv.root
DB_PASSWORD=gSY9SiFI0JHWgiR2
DB_NAME=systemdb

# In app.py
import os
from dotenv import load_dotenv

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')

# In dbcon.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        connection_timeout=300
    )
    return connection
```

---

### 3. No CSRF Protection
**Problem:** Forms vulnerable to CSRF attacks  
**File:** All forms in templates  
**Risk:** High - Malicious sites can submit forms

**Fix:**
```python
# Install Flask-WTF
pip install Flask-WTF

# In app.py
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# In all templates with forms, add:
<form method="POST">
    {{ csrf_token() }}
    <!-- rest of form -->
</form>
```

---

### 4. Database Connection Not Closed Properly
**Problem:** Multiple places don't close connections  
**File:** `app.py` - almost every route  
**Risk:** Medium - Connection pool exhaustion

**Fix:**
```python
# Use context manager pattern
# Replace all instances like this:

# OLD CODE:
mydb = get_db_connection()
mycursor = mydb.cursor()
mycursor.execute("SELECT ...")
results = mycursor.fetchall()
mycursor.close()
mydb.close()

# NEW CODE:
try:
    mydb = get_db_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT ...")
    results = mycursor.fetchall()
except mysql.connector.Error as err:
    print(f"Database error: {err}")
    flash('Database error occurred', 'error')
finally:
    if mycursor:
        mycursor.close()
    if mydb:
        mydb.close()
```

---

## ⚠️ HIGH PRIORITY

### 5. Duplicate Feedback Prevention
**Problem:** Students can submit feedback multiple times  
**File:** `app.py` - `/add_feed` route  
**Risk:** Medium - Data integrity compromised

**Fix:**
```python
# Add new table for feedback tracking
CREATE TABLE feedback_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dept_id INT,
    cd_id INT,
    div_id INT,
    batch_id INT,
    sem INT,
    part INT,
    submission_ip VARCHAR(45),
    submission_time DATETIME,
    UNIQUE KEY unique_submission (dept_id, cd_id, div_id, batch_id, sem, part)
);

# In /add_feed route, before processing:
dept = request.form['dept_id']
cls = request.form['cls_id']
div = request.form['div_id']
batch = session.get('batch_id')  # Store in session during verification
sem = session.get('semester')
part = session.get('part')

cursor = mydb.cursor()
cursor.execute("""
    SELECT id FROM feedback_submissions 
    WHERE dept_id=%s AND cd_id=%s AND div_id=%s AND batch_id=%s AND sem=%s AND part=%s
""", (dept, cls, div, batch, sem, part))

if cursor.fetchone():
    flash('You have already submitted feedback!', 'error')
    return redirect('/thankyou')

# After successful submission:
cursor.execute("""
    INSERT INTO feedback_submissions 
    (dept_id, cd_id, div_id, batch_id, sem, part, submission_ip, submission_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
""", (dept, cls, div, batch, sem, part, request.remote_addr))
mydb.commit()
```

---

### 6. No Input Validation
**Problem:** No server-side validation on forms  
**File:** All routes with `request.form`  
**Risk:** Medium - Invalid data in database

**Fix:**
```python
# Example for add_user route
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validation
        if not name or len(name) < 3:
            flash('Name must be at least 3 characters', 'error')
            return redirect('/user')
        
        if not email or '@' not in email:
            flash('Invalid email address', 'error')
            return redirect('/user')
        
        # Check for duplicate email
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            flash('Email already exists', 'error')
            return redirect('/user')
        
        # Continue with insertion...
```

---

### 7. SQL Injection in Teaching Record Query
**Problem:** SQL query has potential injection point  
**File:** `app.py` line ~776 in `/feedback` route  
**Risk:** High - Database compromise

**Current Code:**
```python
cursor.execute("SELECT ... WHERE ... OR teaching_rec.bat_id LIKE %s", 
               (did, sem, cid, ddid, '%' + bid + '%'))
```

**Fix:**
```python
# The LIKE clause is properly parameterized, but ensure bid is sanitized
bid = ',' + str(int(bat)) + ','  # Ensure it's an integer
```

---

### 8. Session Timeout Not Configured
**Problem:** Sessions never expire  
**File:** `app.py`  
**Risk:** Medium - Session hijacking

**Fix:**
```python
from datetime import timedelta

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['SESSION_COOKIE_SECURE'] = True  # Only if using HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# In login route:
session.permanent = True
```

---

## 📋 MEDIUM PRIORITY

### 9. Error Handling Missing
**Problem:** No try-catch blocks around database operations  
**File:** Throughout `app.py`

**Fix:**
```python
# Add error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='Internal server error'), 500

# Wrap database operations
from functools import wraps

def handle_db_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash('Database error occurred. Please try again.', 'error')
            return redirect(request.referrer or '/')
    return decorated_function

@app.route('/example')
@handle_db_errors
def example():
    # Database operations here
```

---

### 10. DateTime Validation Missing
**Problem:** No check if end_time > start_time  
**File:** `app.py` - `/student_login` route

**Fix:**
```python
start_date_time = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M')
end_date_time = datetime.strptime(end_date_time_str, '%Y-%m-%dT%H:%M')

# Add validation
if end_date_time <= start_date_time:
    flash('End time must be after start time', 'error')
    return redirect('/admin')

if start_date_time < datetime.now():
    flash('Start time cannot be in the past', 'error')
    return redirect('/admin')
```

---

### 11. No Logging System
**Problem:** Can't debug production issues  
**File:** `app.py`

**Fix:**
```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
if not app.debug:
    file_handler = RotatingFileHandler('feedback_system.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Feedback System startup')

# Use in routes
app.logger.info(f'User {email} logged in')
app.logger.error(f'Database error: {err}')
```

---

### 12. Code Duplication
**Problem:** Database connection code repeated everywhere  
**File:** `app.py`

**Fix:**
```python
# Create helper function at top of app.py
def get_cursor():
    """Get database cursor with automatic connection management"""
    mydb = get_db_connection()
    return mydb, mydb.cursor()

def close_db(mydb, cursor):
    """Close database connection and cursor"""
    if cursor:
        cursor.close()
    if mydb:
        mydb.close()

# Usage in routes
mydb, cursor = get_cursor()
try:
    cursor.execute("SELECT ...")
    results = cursor.fetchall()
    mydb.commit()
except Exception as e:
    mydb.rollback()
    raise e
finally:
    close_db(mydb, cursor)
```

---

## 🔧 LOW PRIORITY (Code Quality)

### 13. Global Variables Used
**Problem:** `post_value` and `did` are global  
**File:** `app.py` lines 40-41

**Fix:**
```python
# Remove global variables
# Store in session instead

# In login route:
session['post'] = user[7]
session['did'] = user[3]

# Use session everywhere else
if session.get('post') == 'Admin':
    # Admin logic
```

---

### 14. Dead Code
**Problem:** Commented out code and unused imports  
**File:** `app.py`, `db.py`

**Fix:**
```python
# Remove:
# - MongoDB imports (lines in db.py)
# - Commented database connections
# - Commented PostgreSQL code (lines 18-25)
# - Unused subprocess import (if backup doesn't work)
```

---

### 15. Inconsistent Batch ID Format
**Problem:** Sometimes "0", sometimes ",29,30,"  
**File:** Teaching record queries

**Fix:**
```python
# Standardize to always use comma format
# Update teaching_rec.bat_id:
# - For theory: NULL instead of "0"
# - For practical/tutorial: ",29,30,"

# Update queries:
WHERE (teaching_rec.bat_id IS NULL OR teaching_rec.bat_id LIKE %s)
```

---

## 📊 Testing Checklist After Fixes

- [ ] Login with correct credentials
- [ ] Login with wrong credentials (should fail)
- [ ] Password reset (if added)
- [ ] Feedback submission as student
- [ ] Try duplicate feedback (should block)
- [ ] Schedule feedback with invalid dates
- [ ] Add department with duplicate name
- [ ] SQL injection attempts on forms
- [ ] CSRF attack simulation
- [ ] Session timeout testing
- [ ] Error page display
- [ ] Database connection failure handling
- [ ] All CRUD operations
- [ ] Report generation
- [ ] Excel upload/download

---

## 🚀 Deployment Checklist

- [ ] Change all default passwords
- [ ] Update .env with production credentials
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set debug=False in production
- [ ] Setup database backups
- [ ] Configure firewall rules
- [ ] Setup monitoring/alerts
- [ ] Create admin documentation
- [ ] Test with production data volume
- [ ] Load testing
- [ ] Security audit
- [ ] Create restore procedure

---

## 📝 Quick Fix Priority Order

1. **Password hashing** (30 min)
2. **Environment variables** (20 min)
3. **CSRF protection** (15 min)
4. **Duplicate feedback prevention** (45 min)
5. **Input validation** (1-2 hours)
6. **Error handling** (1 hour)
7. **Session security** (15 min)
8. **Logging** (30 min)
9. **Code cleanup** (1 hour)
10. **Testing** (2-3 hours)

**Total Estimated Time:** 8-10 hours

---

## 🎯 After Fixing

1. Update README.md with new setup instructions
2. Create CHANGELOG.md documenting all fixes
3. Tag release as v2.0
4. Deploy to staging environment
5. Conduct user acceptance testing
6. Deploy to production
7. Monitor logs for 1 week

---

*Remember: Test each fix individually before combining!*
*Keep backups before making changes!*
