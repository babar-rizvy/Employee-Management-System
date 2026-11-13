from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class JobRole(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    class EmploymentStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        ON_LEAVE = "ON_LEAVE", "On leave"

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="employees")
    job_role = models.ForeignKey(JobRole, on_delete=models.PROTECT, related_name="employees")
    skills = models.ManyToManyField(Skill, blank=True, related_name="employees")
    status = models.CharField(max_length=12, choices=EmploymentStatus.choices, default=EmploymentStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["employee_id"]

    def clean(self):
        super().clean()
        if self.salary is not None and self.salary < 0:
            raise ValidationError({"salary": "Salary cannot be negative."})
        if self.hire_date and self.hire_date > timezone.localdate():
            raise ValidationError({"hire_date": "Hire date cannot be in the future."})
        if self.job_role_id and self.salary is not None:
            role = self.job_role
            if self.salary < role.minimum_salary:
                raise ValidationError({
                    "salary": f"Salary must be at least {role.minimum_salary} for this job role."
                })

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="profile")
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    bank_account_last_four = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return f"Profile: {self.employee}"


class Attendance(models.Model):
    class AttendanceStatus(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"
        REMOTE = "REMOTE", "Remote"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(fields=["employee", "date"], name="unique_employee_attendance_per_day")
        ]

    def clean(self):
        super().clean()
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError({"check_out": "Check-out time must be later than check-in time."})

    def __str__(self):
        return f"{self.employee} - {self.date} ({self.status})"


class LeaveRequest(models.Model):
    class LeaveType(models.TextChoices):
        ANNUAL = "ANNUAL", "Annual"
        SICK = "SICK", "Sick"
        PERSONAL = "PERSONAL", "Personal"
        UNPAID = "UNPAID", "Unpaid"

    class LeaveStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=10, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LeaveStatus.choices, default=LeaveStatus.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-applied_at"]

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date cannot be earlier than start date."})

    def __str__(self):
        return f"{self.employee} - {self.leave_type}: {self.start_date} to {self.end_date}"
