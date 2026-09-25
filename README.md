# Rentify – Django Rental Management System

Rentify is a Django-based rental management web application.

## 🛠️ Technologies Used

* Python
* Django
* HTML5
* CSS3
* JavaScript
* Bootstrap
* SQLite / PostgreSQL
* Git & GitHub

---

# 🚀 How to Run the Project

## 1. Clone the Repository

Open Command Prompt or PowerShell and run:

```bash
git clone https://github.com/Rahuldev007-ai/rentify.git
```

Then enter the project folder:

```bash
cd rentify
```

---

## 2. Check Python Installation

Make sure Python is installed:

```bash
python --version
```

Recommended Python version:

```text
Python 3.12+
```

If `python` does not work on Windows, try:

```bash
py --version
```

---

## 3. Create a Virtual Environment

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

After activation, you should see:

```text
(venv)
```

at the beginning of the terminal.

---

## 4. Install Required Packages

Install all project dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install Django manually:

```bash
pip install django
```

---

## 5. Configure Environment Variables

If the project contains a `.env.example` file, create a `.env` file from it.

On Windows Command Prompt:

```bash
copy .env.example .env
```

Then open `.env` and add the required values.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

Do not upload your real `.env` file to GitHub if it contains passwords, API keys, email passwords, or other secrets.

---

## 6. Apply Database Migrations

Run:

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

---

## 7. Create Admin User

Create a Django admin account:

```bash
python manage.py createsuperuser
```

Enter:

```text
Username:
Email:
Password:
Password (again):
```

The password will not be displayed while typing. This is normal.

---

## 8. Run the Development Server

Start the Django server:

```bash
python manage.py runserver
```

You should see something similar to:

```text
Starting development server at http://127.0.0.1:8000/
```

Open this in your browser:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Django Admin

To access the Django admin panel:

```text
http://127.0.0.1:8000/admin/
```

Use the username and password created with:

```bash
python manage.py createsuperuser
```

---

# 📁 Common Project Commands

### Start server

```bash
python manage.py runserver
```

### Create migrations

```bash
python manage.py makemigrations
```

### Apply migrations

```bash
python manage.py migrate
```

### Create superuser

```bash
python manage.py createsuperuser
```

### Open Django shell

```bash
python manage.py shell
```

### Collect static files

```bash
python manage.py collectstatic
```

---

# 🛑 Stop the Server

Press:

```text
CTRL + C
```

---

# 🔄 If You Download the Project Again

If the repository has already been cloned:

```bash
cd rentify
git pull origin main
```

Then activate the virtual environment:

```bash
venv\Scripts\activate
```

Install/update dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run:

```bash
python manage.py runserver
```

---

# 👨‍💻 Developer

Rahul Chanpura

GitHub:

https://github.com/Rahuldev007-ai
