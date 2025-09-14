
# ADA-1 (Asset Document Archive 1)

**ADA-1** is a secure, web-based archive system for managing and viewing classified documents based on user clearance levels. Built using Flask and SQLite, ADA-1 features a dark, CLI-style interface and strict role-based access control.

---

## 🚀 Features

- Terminal-style startup screen requiring secret phrase access
- User registration and login with clearance-based access
- Role-based UI: Admin vs. Regular user
- Add, view, edit, and delete ADA entries (admin only)
- Redacted view for restricted users
- Changelog system for edit history
- Admin panel for user management
- Fully themed SCP-inspired dark UI

---

## 🛠️ Technologies Used

- Python 3.x  
- Flask (backend framework)  
- SQLite (relational database)  
- SQLAlchemy (ORM)  
- Jinja2 (templating)  
- Bootstrap 5 (frontend)  
- Git / GitHub (version control)

---

## 📦 Local installation

### Step-by-step setup:

```bash
# Clone the repo
git clone https://github.com/yourusername/ada1.git
cd ada1

# Set up virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python run.py
📍 The application runs on http://127.0.0.1:5050

🔐 Startup Login Sequence
When launching ADA-1, you'll first encounter a CLI-style boot screen. This should be disabled for testing and evaluation purposes. In the event the startup is not disabled, the following exchange is required to proceed:

Prompt: Does the Black Moon Howl?

Required Answer: Only at the blind (not case sensitive)

Incorrect phrases will return an ACCESS DENIED message and reload the challenge.

Admin Credentials (for testing)
admin credentials for testing as as follows:
Username: admin
Password: admin123

User Guide
1. Startup
Users are prompted to input a secret phrase to access the login page.

2. Login/Register
Users can create accounts and are assigned a clearance level (1–5). Admins are assigned manually.

3. Dashboard
Admins see all documents and options to add/edit/delete entries

Regular users only see entries at or below their clearance

Each document is presented with redacted or full content

4. Asset Entry
Admins can:

Create a new ADA document

Set title, full content, redacted summary, and required clearance level

Edit or delete existing entries

5. Changelog
Every edit made to an asset is logged in the changelog, which appears on each asset detail page.

6. Admin Panel
Admins can:

View a table of all users

Edit usernames, roles, and clearance levels

Delete users (except their own account)

File Structure

ada1/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   └── templates/
│       └── [HTML templates]
├── static/
│   └── [CSS, assets]
├── run.py
├── requirements.txt
└── README.md
📎 Notes
Admin functions are only available to users with the admin role.

Clearance levels range from 1 (lowest) to 5 (highest).

Redacted documents are visible only to users with insufficient clearance.

All changes to entries are logged and timestamped.

Testing
Includes at least 10 users and 10 entries (seeded via Flask shell or script)

Admin UI tested on Chrome and Firefox

Follows assignment criteria: ERD, annotated screenshots, 2+ relational tables

📄 License
This project is for educational purposes as part of a university software engineering module. No external use is permitted without author permission.
