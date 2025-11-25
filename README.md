# 🎓 Faculty Feedback Management System

A comprehensive web-based application for managing student feedback on faculty members in educational institutions. Built with Flask, this system streamlines the feedback collection process, provides detailed analytics, and generates automated reports for faculty performance evaluation.

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [User Roles & Features](#-user-roles--features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
  - [Development Setup](#development-setup)
  - [Production Deployment](#production-deployment)
- [Database Configuration](#-database-configuration)
- [Demo Credentials](#-demo-credentials)
- [Recent Improvements](#-recent-improvements)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Project Overview

The Faculty Feedback Management System is a modern, full-featured web application designed to digitize and automate the faculty evaluation process in colleges and universities. It enables students to provide structured feedback on their instructors while giving administrators powerful tools to analyze performance, generate reports, and make data-driven decisions.

**Key Benefits:**
- 📊 Real-time analytics and performance tracking
- 🔒 Secure, role-based access control
- 📱 Responsive design for mobile and desktop
- 📈 Automated report generation
- 🎨 Modern UI with dark/light mode support
- ⚡ Fast and optimized feedback submission

## ✨ Key Features

### For Students
- ✅ Simple, intuitive feedback forms
- 🔐 Secure access via verification codes
- 💾 Auto-save progress (survives page reload)
- 📝 Multi-question feedback with A/B/C/D ratings
- 💬 Additional comments section
- ⏱️ Fast submission (1-2 seconds)
- 🔄 Real-time progress indicator

### For Administrators
- 👥 Complete user management (Admin/Sub-Admin roles)
- 🏢 Department, class, division, and batch management
- 👨‍🏫 Faculty profile management (individual or bulk upload)
- 📚 Subject and teaching record management
- ❓ Customizable feedback questions (up to 10)
- 📊 Advanced analytics dashboard with charts
- 📄 Automated report generation (PDF/Print)
- 📧 Feedback letter generation
- 🔍 Search and filter capabilities
- 📤 Excel import/export functionality

### For Sub-Admins
- 🏢 Department-specific access
- 👨‍🏫 Manage faculty within their department
- 📊 View department-specific reports
- 📚 Manage subjects and teaching records
- 👥 Limited user management

## 👥 User Roles & Features

### 1. **Admin (Full Access)**
| Feature | Access |
|---------|--------|
| User Management | ✅ Full Access |
| Department Management | ✅ All Departments |
| Faculty Management | ✅ All Faculties |
| Subject Management | ✅ All Subjects |
| Teaching Records | ✅ All Records |
| Feedback Questions | ✅ Create/Edit/Delete |
| Reports & Analytics | ✅ All Departments |
| Student Verification Codes | ✅ Generate/Manage |

### 2. **Sub-Admin (Department-Limited)**
| Feature | Access |
|---------|--------|
| User Management | ❌ No Access |
| Department Management | 👁️ View Only (Own Department) |
| Faculty Management | ✅ Own Department Only |
| Subject Management | ✅ Own Department Only |
| Teaching Records | ✅ Own Department Only |
| Feedback Questions | 👁️ View Only |
| Reports & Analytics | 👁️ Own Department Only |
| Student Verification Codes | ✅ Generate for Own Department |

### 3. **Student**
| Feature | Access |
|---------|--------|
| Access Feedback Form | ✅ Via Verification Code |
| Submit Feedback | ✅ One-time per session |
| View Results | ❌ No Access |
| Edit After Submission | ❌ No Access |

## 🛠 Technology Stack

**Backend:**
- Python 3.8+
- Flask 2.2.2
- MySQL Connector 8.0.32

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 4.6.2
- Font Awesome 5.15.1
- Chart.js 3.9.1 (Analytics)

**Database:**
- MySQL / TiDB Cloud (MySQL-compatible)

**Additional Libraries:**
- Pandas (Excel processing)
- Gunicorn (Production server)
- Jinja2 (Templating)

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher (or TiDB Cloud account)
- pip (Python package manager)

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/Harsh2504/Mega-project.git
cd Mega-project
```

2. **Create virtual environment**
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database** (see [Database Configuration](#-database-configuration))

5. **Import database schema**
```bash
# Import the SQL schema
mysql -u your_username -p your_database_name < systemdb.sql
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
```
Open browser: http://127.0.0.1:8000
```

### Production Deployment

#### Option 1: Using Gunicorn (Recommended)

1. **Install Gunicorn** (already in requirements.txt)
```bash
pip install gunicorn
```

2. **Run with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**Parameters:**
- `-w 4`: 4 worker processes (adjust based on CPU cores)
- `-b 0.0.0.0:8000`: Bind to all interfaces on port 8000
- `app:app`: Module name and Flask app instance

3. **Using Systemd (Linux)**

Create `/etc/systemd/system/feedback-system.service`:
```ini
[Unit]
Description=Faculty Feedback System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Mega-project
Environment="PATH=/path/to/Mega-project/env/bin"
ExecStart=/path/to/Mega-project/env/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl start feedback-system
sudo systemctl enable feedback-system
```

#### Option 2: Using Nginx + Gunicorn

1. **Configure Nginx** (`/etc/nginx/sites-available/feedback-system`)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/Mega-project/static;
    }
}
```

2. **Enable site and restart Nginx**
```bash
sudo ln -s /etc/nginx/sites-available/feedback-system /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Security Recommendations for Production

1. **Change Secret Key** in `app.py`:
```python
app.secret_key = 'your-secure-random-secret-key-here'
```

2. **Disable Debug Mode**: Ensure `debug=False` in production

3. **Use HTTPS**: Configure SSL certificate (Let's Encrypt recommended)

4. **Set Environment Variables**:
```bash
export FLASK_ENV=production
export DATABASE_URL=mysql://user:pass@host/dbname
```

## 🗄 Database Configuration

### Local MySQL Setup

1. **Edit `dbcon.py`**:
```python
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",      # Change this
        password="your_password",  # Change this
        database="systemdb",       # Your database name
        connect_timeout=300
    )
```

### Cloud Database (TiDB Cloud / MySQL)

1. **Edit `dbcon.py`**:
```python
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="your_cloud_user",
        password="your_cloud_password",
        database="systemdb",
        ssl_ca="/path/to/ca-cert.pem",  # If SSL required
        connect_timeout=300
    )
```

2. **Connection Parameters Explained**:
- `host`: Database server address
- `port`: MySQL port (default 3306, TiDB Cloud uses 4000)
- `user`: Database username
- `password`: Database password
- `database`: Database name
- `connect_timeout`: Timeout in seconds (300 = 5 minutes)

### Database Schema

The `systemdb.sql` file contains the complete schema. Key tables:

- **Users**: Admin and Sub-Admin accounts
- **Department**: Academic departments
- **Class**: Academic classes (FY, SY, TY)
- **Division**: Class divisions
- **Batch**: Practical batches
- **Facility**: Faculty members
- **Subject**: Course subjects
- **Teaching_rec**: Faculty-subject-class assignments
- **Questions**: Feedback questions
- **Feedbacknew**: Student feedback responses
- **Comments**: Additional student comments
- **Student**: Student verification codes

## 🔑 Demo Credentials

### Admin Account
```
Email: harsh2504patil@gmail.com
Password: 123456
```
**Access Level:** Full system access, all features enabled

### Sub-Admin Account
```
Email: xyz@gmail.com
Password: 12345
```
**Access Level:** Department-limited access (Computer Engineering)

### Student Access
Students don't have login credentials. Instead, they use:
1. Verification codes generated by Admin/Sub-Admin
2. Access via `/student_verify` route
3. One-time feedback submission per session

**To generate student codes:**
1. Login as Admin/Sub-Admin
2. Navigate to "Student" section
3. Select Class, Division, Department
4. Click "Generate Code"
5. Share code with students

## 🎉 Recent Improvements

### Performance Optimizations ⚡
- **90% Faster Feedback Submission**: Reduced from 10-15 seconds to 1-2 seconds
  - Moved database cursor creation outside loops
  - Implemented batch INSERT using `executemany()`
  - Single commit at end instead of multiple commits
  - Column checks done once before loop

- **Database Connection Fixes**: Resolved timeout errors
  - Fresh connections for each route
  - Eliminated global connection issues
  - Fixed 5 routes: `/verify`, `/class`, `/department`, `/subject`, `/questions`

### User Experience Enhancements 🎨

#### Modern UI Redesign
- **Consistent Purple Theme** (#695CFE) across all pages
- **Dark/Light Mode Support** with CSS variables
- **Modernized Tables**: All 9+ CRUD tables with:
  - Purple gradient headers
  - Hover animations with scale effects
  - Card-based wrappers with shadows
  - Count badges showing record counts
  - Empty state handling with icons

#### Feedback Form Improvements
- **Auto-Save Progress**: LocalStorage-based persistence
  - Saves every radio button selection
  - Restores on page reload
  - Maintains active tab position
  - Unlocks completed question tabs
- **Loading Indicator**: Professional spinner during submission
- **Enhanced Comments Section**:
  - Modern textarea with focus effects
  - Real-time character counter (0/200)
  - Beautiful submit button with icon
- **Better Validation**:
  - Fixed bypass bug (previously only checked last faculty)
  - Now validates ALL faculty feedback
  - Specific error messages with faculty numbers

### Bug Fixes 🐛
- ✅ Fixed validation bypass allowing incomplete feedback
- ✅ Fixed print functionality after table modernization
- ✅ Fixed radio button vertical alignment issues
- ✅ Fixed tab restoration after page reload
- ✅ Resolved MySQL connection timeout errors
- ✅ Fixed character counter in comments section

### New Features ✨
- **Progress Preservation**: Never lose your work on reload
- **Smart Tab Management**: Resume exactly where you left off
- **Enhanced Error Messages**: Know exactly what's missing
- **Responsive Design**: Works perfectly on mobile and desktop
- **Accessibility**: Better keyboard navigation and screen reader support

## 📸 Screenshots

### Admin Dashboard
> *TODO: Add screenshot of admin dashboard with analytics*

### Faculty Management
> *TODO: Add screenshot of modern faculty table with purple theme*

### Feedback Form (Student View)
> *TODO: Add screenshot of modernized feedback form with tab navigation*

### Analytics Dashboard
> *TODO: Add screenshot of Chart.js analytics with performance graphs*

### Reports Generation
> *TODO: Add screenshot of automated report generation interface*

### Comments Section
> *TODO: Add screenshot of modern comments section with character counter*

### Dark Mode
> *TODO: Add screenshot showing dark mode theme*

**How to add screenshots:**
1. Create `screenshots/` folder in project root
2. Add images with descriptive names
3. Update README with image paths:
```markdown
![Admin Dashboard](screenshots/admin-dashboard.png)
```

## 📁 Project Structure

```
Mega-project/
├── app.py                      # Main Flask application
├── dbcon.py                    # Database connection configuration
├── requirements.txt            # Python dependencies
├── systemdb.sql               # Database schema
├── README.md                  # Project documentation
│
├── templates/                 # HTML templates
│   ├── base.html             # Main layout template
│   ├── basefeedback.html     # Feedback form layout
│   ├── login.html            # Login page
│   ├── admin.html            # Admin dashboard
│   ├── faculty.html          # Faculty management
│   ├── subject.html          # Subject management
│   ├── feedback.html         # Student feedback form
│   ├── report.html           # Reports page
│   ├── allreport.html        # All reports view
│   ├── comments.html         # Comments management
│   ├── department.html       # Department management
│   ├── class.html            # Class management
│   ├── divison.html          # Division management
│   ├── batch.html            # Batch management
│   ├── questions.html        # Questions management
│   ├── user.html             # User management
│   ├── student.html          # Student code generation
│   ├── teaching record.html  # Teaching records
│   ├── thankyou.html         # Feedback confirmation
│   └── error.html            # Error pages
│
├── static/                    # Static files
│   ├── css/
│   │   ├── main.css          # Main stylesheet (modern theme)
│   │   ├── login.css         # Login page styles
│   │   ├── error.css         # Error page styles
│   │   └── verify.css        # Verification page styles
│   ├── js/
│   │   ├── main.js           # Main JavaScript
│   │   ├── login.js          # Login functionality
│   │   ├── error.js          # Error handling
│   │   └── disable-back-button.js
│   ├── images/               # Image assets
│   └── files/                # Uploaded files
│
├── db/                        # Database migration scripts
│   ├── batch.sql
│   ├── class.sql
│   ├── department.sql
│   ├── users.sql
│   └── ... (other table schemas)
│
└── dump/                      # Database backups (MongoDB format)
    └── SystemDB/
        ├── *.bson
        └── *.metadata.json
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Harsh Patil**
- Email: harsh2504patil@gmail.com
- GitHub: [@Harsh2504](https://github.com/Harsh2504)

## 🙏 Acknowledgments

- Bootstrap team for the UI framework
- Chart.js for analytics visualizations
- Font Awesome for icons
- Flask community for excellent documentation

## 📞 Support

For issues, questions, or suggestions:
- 🐛 Open an issue on GitHub
- 📧 Email: harsh2504patil@gmail.com
- 💬 Discussions: Use GitHub Discussions tab

---

**⭐ If you find this project useful, please consider giving it a star!**

