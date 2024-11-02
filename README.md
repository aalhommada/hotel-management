# Hotel Management System

A Django-based hotel management system with room booking capabilities.

## Setup

1. Clone the repository

```bash
git clone [https://github.com/aalhommada/hotel-management.git]
cd hotel_management
```

2. Create a virtual environment

```bash
python -m venv hotel-env
```

3. Activate the virtual environment

```bash
# On Windows:
hotel-env\Scripts\activate

# On macOS/Linux:
source hotel-env/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Run migrations

```bash
python manage.py migrate
```

6. Start the development server

```bash
python manage.py runserver
```

## Features

- Room booking system
- User authentication
- Admin dashboard
- Room management
- Booking management

## Technology Stack

- Django
- HTMX
- Alpine.js
- Tailwind CSS with Flowbite
- SQLite
