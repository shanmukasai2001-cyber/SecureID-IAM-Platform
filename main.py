
"""
IAM Identity Governance Lab
Module 01: User Provisioning Engine

Purpose:
- Validate employee identity information
- Detect duplicate employees
- Assign roles based on department
- Store provisioned identities
- Maintain audit logs

Uses synthetic employee information only.
"""

import csv
import re
from pathlib import Path
from datetime import datetime, timezone

# Project directories
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

USERS_FILE = DATA_DIR / "users.csv"
AUDIT_FILE = DATA_DIR / "audit_logs.csv"

# Department-to-role mapping
ROLE_MAPPING = {
    "IT": {
        "role": "IT_ANALYST",
        "permissions": "SYSTEM_READ"
    },
    "HR": {
        "role": "HR_ANALYST",
        "permissions": "EMPLOYEE_READ"
    },
    "Finance": {
        "role": "FINANCE_ANALYST",
        "permissions": "FINANCIAL_READ"
    },
    "Security": {
        "role": "SECURITY_ANALYST",
        "permissions": "SECURITY_READ"
    }
}

USER_FIELDS = [
    "employee_id",
    "full_name",
    "email",
    "department",
    "job_title",
    "assigned_role",
    "permissions",
    "status"
]

AUDIT_FIELDS = [
    "timestamp",
    "employee_id",
    "action",
    "result",
    "details"
]


def initialize_files():
    """Create data directory and CSV files if missing."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_path, fields in [
        (USERS_FILE, USER_FIELDS),
        (AUDIT_FILE, AUDIT_FIELDS)
    ]:
        if not file_path.exists():
            with file_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()


def write_audit_log(employee_id, action, result, details):
    """Record provisioning activities."""

    initialize_files()

    with AUDIT_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=AUDIT_FIELDS)

        writer.writerow({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "employee_id": employee_id,
            "action": action,
            "result": result,
            "details": details
        })


def validate_employee(employee):
    """Validate mandatory employee attributes."""

    required_fields = [
        "employee_id",
        "full_name",
        "email",
        "department",
        "job_title"
    ]

    for field in required_fields:
        if not str(employee.get(field, "")).strip():
            return False, f"Missing required field: {field}"

    email = employee["email"].strip()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Invalid email address"

    if employee["department"] not in ROLE_MAPPING:
        return False, "Department is not authorized for provisioning"

    return True, "Employee validation successful"


def check_duplicate(employee_id, email):
    """Check whether employee ID or email already exists."""

    if not USERS_FILE.exists():
        return False

    with USERS_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for user in reader:
            if (
                user["employee_id"].lower() == employee_id.lower()
                or user["email"].lower() == email.lower()
            ):
                return True

    return False


def provision_user(employee):
    """Provision a new employee identity."""

    initialize_files()

    employee_id = str(employee.get("employee_id", "")).strip()
    email = str(employee.get("email", "")).strip()

    valid, message = validate_employee(employee)

    if not valid:
        write_audit_log(
            employee_id,
            "USER_PROVISIONING",
            "FAILED",
            message
        )
        print(f"[FAILED] {message}")
        return False

    if check_duplicate(employee_id, email):
        write_audit_log(
            employee_id,
            "USER_PROVISIONING",
            "REJECTED",
            "Duplicate employee ID or email"
        )
        print("[REJECTED] Duplicate identity detected")
        return False

    access = ROLE_MAPPING[employee["department"]]

    user_record = {
        "employee_id": employee_id,
        "full_name": employee["full_name"].strip(),
        "email": email.lower(),
        "department": employee["department"],
        "job_title": employee["job_title"].strip(),
        "assigned_role": access["role"],
        "permissions": access["permissions"],
        "status": "ACTIVE"
    }

    with USERS_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=USER_FIELDS)
        writer.writerow(user_record)

    write_audit_log(
        employee_id,
        "USER_PROVISIONING",
        "SUCCESS",
        f"Assigned role: {access['role']}"
    )

    print("\n[SUCCESS] User provisioned successfully")
    print(f"Employee ID : {employee_id}")
    print(f"Name        : {user_record['full_name']}")
    print(f"Department  : {user_record['department']}")
    print(f"Role        : {user_record['assigned_role']}")
    print(f"Permissions : {user_record['permissions']}")

    return True


if __name__ == "__main__":

    # Synthetic employee for testing
    test_employee = {
        "employee_id": "EMP1001",
        "full_name": "Alex Johnson",
        "email": "alex.johnson@example.com",
        "department": "IT",
        "job_title": "IT Support Analyst"
    }

    provision_user(test_employee)
