# Authentication System Guide

## Overview

The Farmer Market Advisor now has a complete authentication system with:
- Landing page for visitors
- User registration
- User login/logout
- Protected dashboard for authenticated users

## Features Implemented

### 1. Landing Page (`/`)
- Attractive hero section with call-to-action buttons
- Feature highlights (Fair Price Analysis, Market Recommendations, Explainable AI)
- Benefits overview
- Responsive design with Bootstrap 5

### 2. Registration Page (`/register/`)
- User-friendly registration form
- Username and password fields with validation
- Password strength requirements
- Automatic login after successful registration
- Redirect to dashboard after registration

### 3. Login Page (`/login/`)
- Simple login form with username and password
- Error messages for invalid credentials
- Success messages on successful login
- Redirect to dashboard after login

### 4. Dashboard (`/dashboard/`)
- Protected route (requires authentication)
- Welcome message with username
- Market recommendation form with:
  - Crop type selection
  - Location input
  - Quantity input
- Quick tips and how-it-works guide
- Recent queries section (placeholder for future implementation)

### 5. Logout (`/logout/`)
- Logs out the user
- Redirects to landing page
- Success message confirmation

## How to Use

### Starting the Server

1. Make sure you're in the project directory
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
3. Open your browser and visit: `http://localhost:8000`

### Testing the Authentication Flow

1. **Visit Landing Page**: Go to `http://localhost:8000`
   - You'll see the landing page with features and benefits
   - Click "Get Started" or "Register" button

2. **Register a New Account**:
   - Fill in username (e.g., "farmer1")
   - Enter a password (must meet Django's requirements)
   - Confirm password
   - Click "Register"
   - You'll be automatically logged in and redirected to dashboard

3. **Access Dashboard**:
   - After login, you'll see the dashboard
   - Fill in the market recommendation form:
     - Select crop type (Wheat, Rice, Tomato, etc.)
     - Enter your location
     - Enter quantity in kg
   - Click "Get Recommendations" (functionality to be implemented)

4. **Logout**:
   - Click "Logout" in the navigation bar
   - You'll be redirected to the landing page

5. **Login Again**:
   - Click "Login" button
   - Enter your username and password
   - Click "Login"
   - You'll be redirected to dashboard

## Technical Details

### URL Structure

- `/` - Landing page (public)
- `/register/` - Registration page (public)
- `/login/` - Login page (public)
- `/logout/` - Logout action (requires authentication)
- `/dashboard/` - Main dashboard (requires authentication)

### Authentication Protection

The dashboard uses Django's `LoginRequiredMixin` to ensure only authenticated users can access it. Unauthenticated users are redirected to the login page.

### Session Management

- Sessions are stored in the database
- Session cookie age: 30 days (configurable in settings)
- Secure session handling with Django's built-in authentication

### Templates

All templates extend from `base.html` which includes:
- Bootstrap 5 for styling
- Bootstrap Icons for icons
- Responsive navigation bar
- Flash messages for user feedback
- Consistent footer

### Styling

- Primary color: Green (#2e7d32) - represents agriculture
- Bootstrap 5 components for modern UI
- Mobile-responsive design
- Clean, farmer-friendly interface

## Next Steps

To complete the application, you'll need to implement:

1. **Market Recommendation Logic**:
   - Process form submission in dashboard
   - Integrate with AI analysis
   - Display recommendations

2. **Query History**:
   - Store user queries in database
   - Display past queries on dashboard
   - Allow users to view historical recommendations

3. **User Profile**:
   - Add user profile page
   - Allow users to update their information
   - Store farmer-specific data (location, crops, etc.)

4. **Enhanced Features**:
   - Email verification
   - Password reset functionality
   - User preferences
   - Notification system

## Testing

Run the authentication tests:
```bash
python test_auth.py
```

All tests should pass, confirming:
- Landing page loads
- Registration works
- Login works
- Dashboard is protected
- Logout works

## Troubleshooting

### Issue: "ALLOWED_HOSTS" error
**Solution**: Make sure `testserver` is in ALLOWED_HOSTS in settings.py

### Issue: "No such table: auth_user"
**Solution**: Run migrations:
```bash
python manage.py migrate
```

### Issue: Redis connection error
**Solution**: The app now uses database sessions by default. If you want to use Redis, make sure Redis server is running.

## Security Notes

- Passwords are hashed using Django's default PBKDF2 algorithm
- CSRF protection is enabled on all forms
- Session cookies are secure
- SQL injection protection via Django ORM
- XSS protection via Django template escaping

## Customization

### Changing Colors

Edit the CSS variables in `templates/base.html`:
```css
:root {
    --primary-color: #2e7d32;
    --secondary-color: #558b2f;
    --accent-color: #ff6f00;
}
```

### Adding More Crop Types

Edit the crop type dropdown in `templates/core/dashboard.html`:
```html
<option value="YourCrop">Your Crop</option>
```

### Modifying Session Duration

Edit `SESSION_COOKIE_AGE` in `config/settings.py` or `.env` file:
```python
SESSION_COOKIE_AGE = 2592000  # 30 days in seconds
```

## Support

For issues or questions:
1. Check the Django documentation: https://docs.djangoproject.com/
2. Review the code comments in views.py and models.py
3. Run tests to verify functionality

---

**Status**: ✅ Authentication system fully functional and tested
**Last Updated**: March 2, 2026
