# Generated for the Employee Management System project.
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="JobRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("minimum_salary", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={"ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_id", models.CharField(max_length=20, unique=True)),
                ("first_name", models.CharField(max_length=60)),
                ("last_name", models.CharField(max_length=60)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("hire_date", models.DateField()),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ("status", models.CharField(choices=[("ACTIVE", "Active"), ("INACTIVE", "Inactive"), ("ON_LEAVE", "On leave")], default="ACTIVE", max_length=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("department", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="employees", to="employees.department")),
                ("job_role", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="employees", to="employees.jobrole")),
                ("skills", models.ManyToManyField(blank=True, related_name="employees", to="employees.skill")),
            ],
            options={"ordering": ["employee_id"]},
        ),
        migrations.CreateModel(
            name="EmployeeProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("address", models.TextField(blank=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("emergency_contact", models.CharField(blank=True, max_length=20)),
                ("bank_account_last_four", models.CharField(blank=True, max_length=4)),
                ("employee", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="employees.employee")),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("check_in", models.TimeField(blank=True, null=True)),
                ("check_out", models.TimeField(blank=True, null=True)),
                ("status", models.CharField(choices=[("PRESENT", "Present"), ("ABSENT", "Absent"), ("LATE", "Late"), ("REMOTE", "Remote")], default="PRESENT", max_length=10)),
                ("notes", models.CharField(blank=True, max_length=255)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_records", to="employees.employee")),
            ],
            options={"ordering": ["-date"]},
        ),
        migrations.CreateModel(
            name="LeaveRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("leave_type", models.CharField(choices=[("ANNUAL", "Annual"), ("SICK", "Sick"), ("PERSONAL", "Personal"), ("UNPAID", "Unpaid")], max_length=10)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("reason", models.TextField()),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")], default="PENDING", max_length=10)),
                ("applied_at", models.DateTimeField(auto_now_add=True)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="leave_requests", to="employees.employee")),
            ],
            options={"ordering": ["-applied_at"]},
        ),
        migrations.AddConstraint(
            model_name="attendance",
            constraint=models.UniqueConstraint(fields=("employee", "date"), name="unique_employee_attendance_per_day"),
        ),
    ]
