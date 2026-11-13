from datetime import date, time, timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Department, JobRole, Skill, Employee, Attendance, LeaveRequest


class EmployeeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(name="Engineering")
        self.role = JobRole.objects.create(title="Developer", minimum_salary=30000)
        self.skill = Skill.objects.create(name="Python")
        self.employee = Employee.objects.create(
            employee_id="EMP001", first_name="Amin", last_name="Rahman",
            email="amin@example.com", hire_date=date.today() - timedelta(days=30),
            salary=45000, department=self.department, job_role=self.role,
        )
        self.employee.skills.add(self.skill)

    def test_employee_list_is_paginated(self):
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)

    def test_employee_search(self):
        response = self.client.get("/api/employees/?search=Amin")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_employee_create_rejects_salary_below_role_minimum(self):
        payload = {
            "employee_id": "EMP002", "first_name": "Nila", "last_name": "Akter",
            "email": "nila@example.com", "hire_date": str(date.today() - timedelta(days=1)),
            "salary": "10000", "department": self.department.id, "job_role": self.role.id,
        }
        response = self.client.post("/api/employees/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("salary", response.data)

    def test_attendance_duplicate_per_day_rejected_by_database(self):
        Attendance.objects.create(employee=self.employee, date=date.today(), status="PRESENT")
        self.assertEqual(Attendance.objects.filter(employee=self.employee, date=date.today()).count(), 1)

    def test_leave_date_validation(self):
        payload = {
            "employee": self.employee.id, "leave_type": "ANNUAL",
            "start_date": str(date.today()), "end_date": str(date.today() - timedelta(days=1)),
            "reason": "Personal leave",
        }
        response = self.client.post("/api/leave-requests/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
