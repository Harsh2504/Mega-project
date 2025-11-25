# Two-Factor Authentication (2FA) Setup Guide

## ✅ What Has Been Implemented

A complete **TOTP-based Two-Factor Authentication** system has been added to your feedback application using:
- **pyotp** - Generates and validates time-based one-time passwords
- **qrcode** - Creates QR codes for easy authenticator app enrollment
- **Google Authenticator / Microsoft Authenticator / Authy** compatibility

## 🔒 Security Features

- **Enhanced Login Security**: Password + 6-digit rotating code from authenticator app
- **Admin-Only by Default**: Currently enabled for Admin users only (can be extended to Sub-Admins)
- **Encrypted Secrets**: TOTP secrets stored securely in database
- **Session Protection**: Prevents unauthorized access even if password is compromised

## 📋 Database Setup Required

**IMPORTANT**: Before using 2FA, you MUST run this SQL script on your database:

```sql
-- Location: db/add_2fa_columns.sql
ALTER TABLE `users` 
ADD COLUMN `totp_secret` VARCHAR(32) NULL DEFAULT NULL COMMENT 'TOTP secret key for 2FA',
ADD COLUMN `totp_enabled` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '2FA enabled flag (0=disabled, 1=enabled)';
```

### How to Run the SQL Script:

**Option 1: Using phpMyAdmin**
1. Open phpMyAdmin
2. Select `systemdb` database
3. Go to "SQL" tab
4. Copy and paste the contents of `db/add_2fa_columns.sql`
5. Click "Go"

**Option 2: Using MySQL Command Line**
```bash
mysql -u root -p systemdb < db/add_2fa_columns.sql
```

**Option 3: Using your database management tool**
- Open the SQL file in your preferred database tool
- Execute it against the `systemdb` database

## 🚀 How to Enable 2FA (Admin)

### Step 1: Login as Admin
- Go to your application login page
- Enter your email and password

### Step 2: Access 2FA Setup
- Click on your **account icon** (top-right)
- Select **"Two-Factor Auth"** from the dropdown menu
- OR directly visit: `http://yoursite.com/setup_2fa`

### Step 3: Install Authenticator App
Download one of these apps on your smartphone:
- **Google Authenticator** (iOS/Android) - Most popular
- **Microsoft Authenticator** (iOS/Android) - Feature-rich
- **Authy** (iOS/Android/Desktop) - Cloud backup support

### Step 4: Scan QR Code
1. Open your authenticator app
2. Tap the **+** button to add a new account
3. Select "Scan QR Code"
4. Point your camera at the QR code on the screen

**Alternative**: If QR scan doesn't work, manually enter the **secret key** shown below the QR code

### Step 5: Verify Setup
1. The authenticator app will show a **6-digit code** that refreshes every 30 seconds
2. Enter this code in the verification box
3. Click **"Enable 2FA"**
4. You'll see a success message!

## 🔐 How Login Works with 2FA

### Normal Login (2FA Disabled)
1. Enter email and password → Login successful

### Enhanced Login (2FA Enabled)
1. Enter email and password
2. If correct, redirected to **2FA verification page**
3. Open authenticator app and get the current **6-digit code**
4. Enter the code
5. Login successful!

**Important**: The code changes every 30 seconds, so use the current one!

## 🛠️ 2FA Management

### Check 2FA Status
- Go to account menu → "Two-Factor Auth"
- You'll see: **"Enabled ✓"** or **"Disabled ✗"**

### Disable 2FA
1. Go to "Two-Factor Auth" page
2. If enabled, you'll see a **"Disable 2FA"** button
3. Click it and confirm
4. 2FA will be turned off (you'll only need password to login)

### Re-enable 2FA
- Just follow the setup steps again
- You'll get a **new QR code** and **new secret key**
- Scan the new QR code with your authenticator app

## 🔄 New Routes Added

| Route | Method | Purpose |
|-------|--------|---------|
| `/setup_2fa` | GET | Show QR code and setup instructions |
| `/verify_2fa_setup` | POST | Verify code and enable 2FA |
| `/verify_2fa` | GET/POST | Verify 2FA code during login |
| `/disable_2fa` | POST | Turn off 2FA for user |

## 📱 Authenticator App Recommendations

### Google Authenticator
- **Pros**: Simple, fast, widely trusted
- **Cons**: No cloud backup (codes lost if phone is lost)
- **Best for**: Users who want simplicity

### Microsoft Authenticator
- **Pros**: Cloud backup, additional features, push notifications
- **Cons**: Requires Microsoft account for backup
- **Best for**: Users who want cloud sync

### Authy
- **Pros**: Cloud backup, multi-device support, desktop app
- **Cons**: Requires phone number for setup
- **Best for**: Users with multiple devices

## 🚨 Troubleshooting

### "Invalid verification code" Error
**Causes**:
1. **Time sync issue**: Phone clock not synchronized
   - **Fix**: Go to phone settings → Date & Time → Enable "Automatic date and time"
2. **Wrong code**: Code expired (they change every 30 seconds)
   - **Fix**: Wait for the next code to appear
3. **Wrong account**: Scanned QR code for different user
   - **Fix**: Delete the entry and scan again

### Lost Phone / Can't Access Authenticator App
**Emergency Disable (Database Method)**:
```sql
-- Run this SQL to disable 2FA for a specific user
UPDATE users 
SET totp_enabled = 0, totp_secret = NULL 
WHERE email = 'admin@example.com';
```

### QR Code Not Scanning
1. **Increase screen brightness**
2. **Try manual entry**: Use the secret key shown below QR code
3. **Take screenshot**: Scan from another device

## 🔧 Technical Details

### Security Implementation
- **Algorithm**: TOTP (Time-based One-Time Password) - RFC 6238
- **Hash**: SHA-1 (industry standard for TOTP)
- **Time Step**: 30 seconds
- **Code Length**: 6 digits
- **Tolerance Window**: ±30 seconds (accepts previous/next code)

### Database Schema
```sql
totp_secret VARCHAR(32)      -- Base32-encoded secret (e.g., "JBSWY3DPEHPK3PXP")
totp_enabled TINYINT(1)      -- 0 = disabled, 1 = enabled
```

### Session Flow
1. User enters password → Stored in `session['pending_2fa_user_id']`
2. User enters 2FA code → Validated against `totp_secret`
3. If valid → Full login, clear pending session
4. If invalid → Show error, remain on verification page

## 📊 Should You Enable 2FA for Sub-Admins?

### Currently Implemented
✅ **Admin users only** - Best for initial deployment

### Extending to Sub-Admins
To enable 2FA for Sub-Admins, update `templates/base.html`:

**Current code** (Admin only):
```html
{% if user == "Admin" %} 
<a href="{{ url_for('setup_2fa') }}" class="sub-link">
    <li class="sub-item">
        <span class="material-icons-outlined">security</span>
        <p>Two-Factor Auth</p>
    </li>
</a>
{% endif %}
```

**Updated code** (Admin + Sub-Admin):
```html
{% if user == "Admin" or user == "Sub-Admin" %} 
<a href="{{ url_for('setup_2fa') }}" class="sub-link">
    <li class="sub-item">
        <span class="material-icons-outlined">security</span>
        <p>Two-Factor Auth</p>
    </li>
</a>
{% endif %}
```

### Recommendation
- **Start with Admin only** - Test thoroughly first
- **Extend to Sub-Admins later** - Once comfortable with the system
- **Make it optional** - Don't force all users to enable it

## ✅ Testing Checklist

Before going live, test these scenarios:

- [ ] Admin can access `/setup_2fa`
- [ ] QR code displays correctly
- [ ] Can scan QR code with authenticator app
- [ ] Manual secret key entry works
- [ ] Verification code validates correctly
- [ ] 2FA gets enabled after verification
- [ ] Login requires 2FA code when enabled
- [ ] Invalid codes are rejected
- [ ] Correct codes allow login
- [ ] Can disable 2FA successfully
- [ ] Can re-enable 2FA (new secret generated)
- [ ] Sub-admins cannot access 2FA (unless extended)

## 🎯 Quick Start Commands

```bash
# 1. Install packages (already done)
pip install pyotp qrcode[pil]

# 2. Run database migration
mysql -u root -p systemdb < db/add_2fa_columns.sql

# 3. Start application
python app.py

# 4. Test as admin
# - Login → Click account menu → "Two-Factor Auth"
# - Scan QR code with Google Authenticator
# - Enter code to enable
# - Logout and login again (will ask for 2FA code)
```

## 📚 Additional Resources

- [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2) (Android)
- [Google Authenticator](https://apps.apple.com/app/google-authenticator/id388497605) (iOS)
- [RFC 6238 - TOTP Spec](https://datatracker.ietf.org/doc/html/rfc6238)
- [pyotp Documentation](https://pyauth.github.io/pyotp/)

## 🤝 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify database migration was successful
3. Check Flask app logs for errors
4. Ensure phone time is synchronized

---

**Security Note**: 2FA significantly improves security but is not unbreakable. Always use strong passwords in combination with 2FA for maximum protection.
