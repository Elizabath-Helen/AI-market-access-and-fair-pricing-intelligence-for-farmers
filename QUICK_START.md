# Quick Start Guide - Farmer Market Advisor

## ✅ Problem Fixed!

The database has been configured correctly and all authentication tables are now created.

## 🚀 Start the Application

### Option 1: Use the Batch File (Windows)
```bash
start_server.bat
```

### Option 2: Manual Start
```bash
python manage.py runserver
```

Then open your browser and visit: **http://localhost:8000**

## 📋 What You Can Do Now

### 1. Register a New Account
- Go to http://localhost:8000
- Click "Get Started" or "Register"
- Fill in:
  - Username (e.g., "farmer1")
  - Password (must be strong)
  - Confirm password
- Click "Register"
- You'll be automatically logged in!

### 2. Login
- Go to http://localhost:8000/login/
- Enter your username and password
- Click "Login"
- You'll be redirected to the dashboard

### 3. Access Dashboard
- After login, you'll see the dashboard at http://localhost:8000/dashboard/
- Fill in the form:
  - Select crop type (Wheat, Rice, Tomato, etc.)
  - Enter your location
  - Enter quantity in kg
- Click "Get Recommendations"

### 4. Logout
- Click "Logout" in the navigation bar
- You'll be redirected to the landing page

## 🗄️ Database Information

**Database Type**: SQLite (for development)
**Database File**: `db.sqlite3` (in project root)
**Tables Created**: 17 tables including:
- `auth_user` - User accounts
- `auth_group` - User groups
- `auth_permission` - Permissions
- `django_session` - User sessions
- `farmer_queries` - Query history
- `markets` - Market data
- `market_prices` - Price data
- And more...

## ✅ Verification

All authentication tests passed:
- ✓ Landing page loads
- ✓ Registration works
- ✓ Login works
- ✓ Dashboard is protected
- ✓ Logout works
- ✓ All database tables created

## 🔧 Troubleshooting

### If you see "no such table" error:
```bash
python manage.py migrate
```

### To verify tables are created:
```bash
python verify_auth_tables.py
```

### To run all tests:
```bash
python test_auth.py
```

## 📝 Test Credentials

You can create any username/password combination. For testing:
- Username: `testfarmer`
- Password: `TestPass123!`

## 🎨 Features

- ✅ Beautiful landing page
- ✅ User registration with validation
- ✅ Secure login system
- ✅ Protected dashboard
- ✅ Session management
- ✅ Responsive design (mobile-friendly)
- ✅ Flash messages for feedback
- ✅ CSRF protection
- ✅ Password hashing

## 📚 Next Steps

The authentication system is complete and working. You can now:
1. Start the server and test registration/login
2. Implement the market recommendation logic
3. Add query history functionality
4. Integrate AI analysis
5. Connect to real market data APIs

## 🆘 Need Help?

Check these files:
- `AUTHENTICATION_GUIDE.md` - Detailed authentication documentation
- `README.md` - Project overview
- `MIGRATION_VERIFICATION.md` - Database schema details

---

**Status**: ✅ All systems ready!
**Last Updated**: March 2, 2026
