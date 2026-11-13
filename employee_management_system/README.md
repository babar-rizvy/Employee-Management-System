# Employee Management System

A Django REST Framework backend project for managing employees, departments, job roles, skills, employee profiles, attendance, and leave requests.

## 1. Problem Statement

Organizations need a centralized system to maintain employee records, assign departments and job roles, track skills, monitor attendance, and process leave applications. This project provides a relational database and RESTful APIs for these operations.

## 2. Features

- Department, job role, and skill management.
- Employee CRUD with department and job-role assignments.
- Many-to-many employee skills.
- One-to-one employee profile.
- Attendance tracking with one record per employee per day.
- Leave application and status management.
- Nested read-only employee details in API responses.
- Field-level, cross-field, and model validation.
- Filtering, searching, ordering, and pagination on list endpoints.
- Customized Django Admin.
- Automated API tests.

## 3. Technologies

- Python 3.10+
- Django 5.x
- Django REST Framework
- django-filter
- SQLite

## 4. Installation

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows
venv\\Scripts\\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 5. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

The project includes an initial migration at `employees/migrations/0001_initial.py`.

## 6. Create Admin User and Run

```bash
python manage.py createsuperuser
python manage.py runserver
```

- API root: http://127.0.0.1:8000/api/
- Admin panel: http://127.0.0.1:8000/admin/

## 7. API Endpoints

All endpoints support standard ModelViewSet actions: GET list, GET detail, POST create, PUT update, PATCH partial update, and DELETE.

| Resource | Endpoint |
|---|---|
| Departments | `/api/departments/` |
| Job roles | `/api/job-roles/` |
| Skills | `/api/skills/` |
| Employees | `/api/employees/` |
| Employee profiles | `/api/employee-profiles/` |
| Attendance | `/api/attendance/` |
| Leave requests | `/api/leave-requests/` |

## 8. Filtering, Searching, Ordering, Pagination

Examples:

```http
GET /api/employees/?department=1
GET /api/employees/?status=ACTIVE
GET /api/employees/?search=Rahman
GET /api/employees/?ordering=-salary
GET /api/employees/?page=2
GET /api/attendance/?status=LATE&ordering=-date
GET /api/leave-requests/?leave_type=SICK&status=PENDING
```

List responses use PageNumberPagination and include `count`, `next`, `previous`, and `results`. Default page size is 10.

## 9. Sample API Requests

### Create a department

`POST /api/departments/`

```json
{
  "name": "Engineering",
  "description": "Software and technology department"
}
```

### Create a job role

`POST /api/job-roles/`

```json
{
  "title": "Software Developer",
  "description": "Develops and maintains applications",
  "minimum_salary": "30000.00"
}
```

### Create a skill

`POST /api/skills/`

```json
{
  "name": "Python",
  "description": "Python programming"
}
```

### Create an employee

`POST /api/employees/`

```json
{
  "employee_id": "EMP001",
  "first_name": "Amin",
  "last_name": "Rahman",
  "email": "amin@example.com",
  "phone": "01700000000",
  "hire_date": "2025-01-15",
  "salary": "45000.00",
  "department": 1,
  "job_role": 1,
  "skills": [1],
  "status": "ACTIVE"
}
```

### Create employee profile

`POST /api/employee-profiles/`

```json
{
  "employee": 1,
  "address": "Chattogram, Bangladesh",
  "date_of_birth": "2000-05-10",
  "emergency_contact": "01800000000",
  "bank_account_last_four": "1234"
}
```

### Create attendance

`POST /api/attendance/`

```json
{
  "employee": 1,
  "date": "2025-02-01",
  "check_in": "09:00:00",
  "check_out": "17:00:00",
  "status": "PRESENT",
  "notes": "Regular office day"
}
```

### Apply for leave

`POST /api/leave-requests/`

```json
{
  "employee": 1,
  "leave_type": "ANNUAL",
  "start_date": "2025-03-10",
  "end_date": "2025-03-12",
  "reason": "Personal work"
}
```

### Example validation error

A salary lower than the selected job role's minimum salary returns HTTP 400 with a field-specific error.

```json
{
  "salary": [
    "Salary must be at least 30000.00 for the selected job role."
  ]
}
```

## 10. API Testing

Run automated tests:

```bash
python manage.py test
```

You can also test endpoints through the DRF Browsable API or import `postman_collection.json` into Postman.

## 11. Notes

- SQLite is configured by default for easy local setup.
- `AllowAny` permissions are used for classroom evaluation and easy Postman testing. For production, add authentication and role-based permissions.
- Change `SECRET_KEY`, disable `DEBUG`, and configure `ALLOWED_HOSTS` before deployment.
