
from datetime import date

from django.contrib.auth import get_user_model
from django.db import transaction

from account.models import (
    Department,
    Asset,
    ServiceCall,
    WorkLog,
)


User = get_user_model()


@transaction.atomic
def seed_data():

    print("Starting demo data insertion...")

    # ==========================================================
    # 1. DEPARTMENTS
    # ==========================================================

    departments = {}

    department_names = [
        "IT",
        "HR",
        "Finance",
        "Operations",
        "Administration",
    ]

    for name in department_names:

        department, created = Department.objects.get_or_create(
            name=name
        )

        departments[name] = department

    print(
        "Departments created/available:",
        len(departments)
    )


    # ==========================================================
    # 2. USERS
    # ==========================================================

    users_data = [
        {
            "username": "admin01",
            "first_name": "System",
            "last_name": "Admin",
            "email": "admin01@example.com",
            "mobile": "9000000001",
            "role": User.Role.ADMIN,
            "department": departments["Administration"],
            "password": "Admin@123",
        },

        {
            "username": "admin02",
            "first_name": "IT",
            "last_name": "Manager",
            "email": "admin02@example.com",
            "mobile": "9000000002",
            "role": User.Role.ADMIN,
            "department": departments["IT"],
            "password": "Admin@123",
        },

        {
            "username": "tech01",
            "first_name": "Rahul",
            "last_name": "Sharma",
            "email": "tech01@example.com",
            "mobile": "9000000003",
            "role": User.Role.TECHNICIAN,
            "department": departments["IT"],
            "password": "Tech@123",
        },

        {
            "username": "tech02",
            "first_name": "Priya",
            "last_name": "Singh",
            "email": "tech02@example.com",
            "mobile": "9000000004",
            "role": User.Role.TECHNICIAN,
            "department": departments["IT"],
            "password": "Tech@123",
        },

        {
            "username": "employee01",
            "first_name": "Ananya",
            "last_name": "Das",
            "email": "employee01@example.com",
            "mobile": "9000000005",
            "role": User.Role.EMPLOYEE,
            "department": departments["HR"],
            "password": "Employee@123",
        },

        {
            "username": "employee02",
            "first_name": "Rohan",
            "last_name": "Roy",
            "email": "employee02@example.com",
            "mobile": "9000000006",
            "role": User.Role.EMPLOYEE,
            "department": departments["Finance"],
            "password": "Employee@123",
        },

        {
            "username": "employee03",
            "first_name": "Neha",
            "last_name": "Gupta",
            "email": "employee03@example.com",
            "mobile": "9000000007",
            "role": User.Role.EMPLOYEE,
            "department": departments["Operations"],
            "password": "Employee@123",
        },

        {
            "username": "employee04",
            "first_name": "Arjun",
            "last_name": "Mehta",
            "email": "employee04@example.com",
            "mobile": "9000000008",
            "role": User.Role.EMPLOYEE,
            "department": departments["Administration"],
            "password": "Employee@123",
        },
    ]

    users = {}

    for data in users_data:

        username = data["username"]
        password = data["password"]

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "email": data["email"],
                "mobile": data["mobile"],
                "role": data["role"],
                "department": data["department"],
            }
        )

        if created:

            user.set_password(password)
            user.save()

        else:

            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]
            user.mobile = data["mobile"]
            user.role = data["role"]
            user.department = data["department"]

            user.save()

        users[username] = user

    # Make sure admin users can access Django admin.

    users["admin01"].is_staff = True
    users["admin01"].is_superuser = True
    users["admin01"].save()

    users["admin02"].is_staff = True
    users["admin02"].save()

    print(
        "Users created/available:",
        len(users)
    )


    # ==========================================================
    # 3. ASSETS
    # ==========================================================

    assets_data = [

        {
            "asset_tag": "AST-LPT-2026-0001",
            "asset_type": Asset.AssetType.LAPTOP,
            "brand": "Dell",
            "model": "Latitude 5440",
            "serial_number": "DL5440SN001",
            "ram": "16 GB",
            "storage": "512 GB SSD",
            "ip_address": None,
            "mac_address": "00:1A:2B:3C:4D:01",
            "purchase_date": date(2026, 1, 15),
            "warranty_expiry": date(2029, 1, 14),
            "status": Asset.Status.ASSIGNED,
            "current_department": departments["HR"],
            "current_custodian": users["employee01"],
            "room_no": "HR-101",
        },

        {
            "asset_tag": "AST-LPT-2026-0002",
            "asset_type": Asset.AssetType.LAPTOP,
            "brand": "HP",
            "model": "ProBook 450 G10",
            "serial_number": "HPP450SN002",
            "ram": "16 GB",
            "storage": "512 GB SSD",
            "ip_address": None,
            "mac_address": "00:1A:2B:3C:4D:02",
            "purchase_date": date(2026, 2, 10),
            "warranty_expiry": date(2029, 2, 9),
            "status": Asset.Status.ASSIGNED,
            "current_department": departments["Finance"],
            "current_custodian": users["employee02"],
            "room_no": "FIN-201",
        },

        {
            "asset_tag": "AST-DES-2026-0003",
            "asset_type": Asset.AssetType.DESKTOP,
            "brand": "Lenovo",
            "model": "ThinkCentre M80",
            "serial_number": "LNM80SN003",
            "ram": "16 GB",
            "storage": "1 TB SSD",
            "ip_address": None,
            "mac_address": "00:1A:2B:3C:4D:03",
            "purchase_date": date(2026, 3, 5),
            "warranty_expiry": date(2029, 3, 4),
            "status": Asset.Status.ASSIGNED,
            "current_department": departments["Operations"],
            "current_custodian": users["employee03"],
            "room_no": "OPS-301",
        },

        {
            "asset_tag": "AST-DES-2026-0004",
            "asset_type": Asset.AssetType.DESKTOP,
            "brand": "HP",
            "model": "EliteDesk 800",
            "serial_number": "HPEDSN004",
            "ram": "16 GB",
            "storage": "512 GB SSD",
            "ip_address": None,
            "mac_address": "00:1A:2B:3C:4D:04",
            "purchase_date": date(2026, 3, 20),
            "warranty_expiry": date(2029, 3, 19),
            "status": Asset.Status.ASSIGNED,
            "current_department": departments["Administration"],
            "current_custodian": users["employee04"],
            "room_no": "ADM-401",
        },

        {
            "asset_tag": "AST-PRN-2026-0005",
            "asset_type": Asset.AssetType.NETWORK_PRINTER,
            "brand": "Canon",
            "model": "imageCLASS LBP",
            "serial_number": "CANONSN005",
            "ram": "",
            "storage": "",
            "ip_address": "192.168.1.105",
            "mac_address": "00:1A:2B:3C:4D:05",
            "purchase_date": date(2026, 4, 1),
            "warranty_expiry": date(2029, 3, 31),
            "status": Asset.Status.IN_STOCK,
            "current_department": departments["IT"],
            "current_custodian": None,
            "room_no": "IT-101",
        },

        {
            "asset_tag": "AST-SCN-2026-0006",
            "asset_type": Asset.AssetType.SCANNER,
            "brand": "Epson",
            "model": "WorkForce ES-500W",
            "serial_number": "EPSONSN006",
            "ram": "",
            "storage": "",
            "ip_address": "192.168.1.106",
            "mac_address": "00:1A:2B:3C:4D:06",
            "purchase_date": date(2026, 4, 15),
            "warranty_expiry": date(2029, 4, 14),
            "status": Asset.Status.IN_STOCK,
            "current_department": departments["IT"],
            "current_custodian": None,
            "room_no": "IT-102",
        },

        {
            "asset_tag": "AST-LPT-2026-0007",
            "asset_type": Asset.AssetType.LAPTOP,
            "brand": "Lenovo",
            "model": "ThinkPad E14",
            "serial_number": "TPE14SN007",
            "ram": "8 GB",
            "storage": "512 GB SSD",
            "ip_address": None,
            "mac_address": "00:1A:2B:3C:4D:07",
            "purchase_date": date(2026, 5, 5),
            "warranty_expiry": date(2029, 5, 4),
            "status": Asset.Status.UNDER_MAINTENANCE,
            "current_department": departments["IT"],
            "current_custodian": None,
            "room_no": "IT-103",
        },

        {
            "asset_tag": "AST-DES-2026-0008",
            "asset_type": Asset.AssetType.DESKTOP,
            "brand": "Dell",
            "model": "OptiPlex 7010",
            "serial_number": "DOPT7010SN008",
            "ram": "8 GB",
            "storage": "512 GB SSD",
            "ip_address": None,
            "mac_address": "00:1A:2B:3C:4D:08",
            "purchase_date": date(2026, 5, 20),
            "warranty_expiry": date(2029, 5, 19),
            "status": Asset.Status.IN_STOCK,
            "current_department": departments["IT"],
            "current_custodian": None,
            "room_no": "IT-104",
        },
    ]

    assets = {}

    for data in assets_data:

        asset, created = Asset.objects.get_or_create(
            asset_tag=data["asset_tag"],
            defaults=data
        )

        assets[asset.asset_tag] = asset

    print(
        "Assets created/available:",
        len(assets)
    )


    # ==========================================================
    # 4. SERVICE CALLS
    # ==========================================================

    service_calls_data = [

        {
            "ticket_id": "CALL-2026-0001",
            "asset": assets["AST-LPT-2026-0001"],
            "reported_by": users["employee01"],
            "assigned_technician": users["tech01"],
            "category": ServiceCall.Category.SOFTWARE_CRASH,
            "description": "Laptop is showing frequent application crashes.",
            "severity": ServiceCall.Severity.MEDIUM,
            "status": ServiceCall.Status.RESOLVED,
            "employee_verified": True,
        },

        {
            "ticket_id": "CALL-2026-0002",
            "asset": assets["AST-LPT-2026-0002"],
            "reported_by": users["employee02"],
            "assigned_technician": users["tech02"],
            "category": ServiceCall.Category.NETWORK,
            "description": "Unable to connect to office Wi-Fi.",
            "severity": ServiceCall.Severity.HIGH,
            "status": ServiceCall.Status.IN_PROGRESS,
            "employee_verified": False,
        },

        {
            "ticket_id": "CALL-2026-0003",
            "asset": assets["AST-DES-2026-0003"],
            "reported_by": users["employee03"],
            "assigned_technician": users["tech01"],
            "category": ServiceCall.Category.HARDWARE_FAILURE,
            "description": "Desktop is not powering on.",
            "severity": ServiceCall.Severity.CRITICAL,
            "status": ServiceCall.Status.ASSIGNED,
            "employee_verified": False,
        },

        {
            "ticket_id": "CALL-2026-0004",
            "asset": assets["AST-DES-2026-0004"],
            "reported_by": users["employee04"],
            "assigned_technician": users["tech02"],
            "category": ServiceCall.Category.HARDWARE_FAILURE,
            "description": "Keyboard keys are not responding.",
            "severity": ServiceCall.Severity.LOW,
            "status": ServiceCall.Status.CLOSED,
            "employee_verified": True,
        },

        {
            "ticket_id": "CALL-2026-0005",
            "asset": assets["AST-PRN-2026-0005"],
            "reported_by": users["admin01"],
            "assigned_technician": users["tech01"],
            "category": ServiceCall.Category.CONSUMABLES,
            "description": "Printer toner needs replacement.",
            "severity": ServiceCall.Severity.MEDIUM,
            "status": ServiceCall.Status.LOGGED,
            "employee_verified": False,
        },

        {
            "ticket_id": "CALL-2026-0006",
            "asset": assets["AST-SCN-2026-0006"],
            "reported_by": users["admin02"],
            "assigned_technician": users["tech02"],
            "category": ServiceCall.Category.HARDWARE_FAILURE,
            "description": "Scanner is producing distorted scans.",
            "severity": ServiceCall.Severity.HIGH,
            "status": ServiceCall.Status.RESOLVED,
            "employee_verified": True,
        },

        {
            "ticket_id": "CALL-2026-0007",
            "asset": assets["AST-LPT-2026-0007"],
            "reported_by": users["admin01"],
            "assigned_technician": users["tech01"],
            "category": ServiceCall.Category.SOFTWARE_CRASH,
            "description": "Operating system freezes during startup.",
            "severity": ServiceCall.Severity.HIGH,
            "status": ServiceCall.Status.IN_PROGRESS,
            "employee_verified": False,
        },

        {
            "ticket_id": "CALL-2026-0008",
            "asset": assets["AST-DES-2026-0008"],
            "reported_by": users["admin02"],
            "assigned_technician": None,
            "category": ServiceCall.Category.NETWORK,
            "description": "Network connection is unavailable.",
            "severity": ServiceCall.Severity.MEDIUM,
            "status": ServiceCall.Status.LOGGED,
            "employee_verified": False,
        },
    ]

    service_calls = {}

    for data in service_calls_data:

        ticket_id = data["ticket_id"]

        service_call, created = ServiceCall.objects.get_or_create(
            ticket_id=ticket_id,
            defaults=data
        )

        service_calls[ticket_id] = service_call

    print(
        "Service calls created/available:",
        len(service_calls)
    )


    # ==========================================================
    # 5. WORK LOGS
    # ==========================================================

    work_logs_data = [

        {
            "service_call": service_calls["CALL-2026-0001"],
            "technician": users["tech01"],
            "description": "Checked application logs and repaired corrupted configuration files.",
        },

        {
            "service_call": service_calls["CALL-2026-0002"],
            "technician": users["tech02"],
            "description": "Checked network adapter and renewed the IP configuration.",
        },

        {
            "service_call": service_calls["CALL-2026-0003"],
            "technician": users["tech01"],
            "description": "Checked power supply and motherboard connections.",
        },

        {
            "service_call": service_calls["CALL-2026-0004"],
            "technician": users["tech02"],
            "description": "Replaced the faulty keyboard and tested all keys.",
        },

        {
            "service_call": service_calls["CALL-2026-0005"],
            "technician": users["tech01"],
            "description": "Checked toner level and prepared replacement cartridge.",
        },

        {
            "service_call": service_calls["CALL-2026-0006"],
            "technician": users["tech02"],
            "description": "Cleaned scanner glass and recalibrated the scanner.",
        },

        {
            "service_call": service_calls["CALL-2026-0007"],
            "technician": users["tech01"],
            "description": "Checked startup services and began operating system diagnostics.",
        },

        {
            "service_call": service_calls["CALL-2026-0008"],
            "technician": users["tech02"],
            "description": "Checked Ethernet cable and network port configuration.",
        },
    ]

    work_logs = []

    for data in work_logs_data:

        work_log, created = WorkLog.objects.get_or_create(
            service_call=data["service_call"],
            technician=data["technician"],
            description=data["description"]
        )

        work_logs.append(work_log)

    print(
        "Work logs created/available:",
        len(work_logs)
    )


    # ==========================================================
    # FINAL OUTPUT
    # ==========================================================

    print("")
    print("==========================================")
    print("DEMO DATA INSERTION COMPLETED")
    print("==========================================")

    print("")
    print("LOGIN CREDENTIALS")

    print("")
    print("ADMIN 1")
    print("Username : admin01")
    print("Password : Admin@123")

    print("")
    print("ADMIN 2")
    print("Username : admin02")
    print("Password : Admin@123")

    print("")
    print("TECHNICIAN 1")
    print("Username : tech01")
    print("Password : Tech@123")

    print("")
    print("TECHNICIAN 2")
    print("Username : tech02")
    print("Password : Tech@123")

    print("")
    print("EMPLOYEE 1")
    print("Username : employee01")
    print("Password : Employee@123")

    print("")
    print("EMPLOYEE 2")
    print("Username : employee02")
    print("Password : Employee@123")

    print("")
    print("EMPLOYEE 3")
    print("Username : employee03")
    print("Password : Employee@123")

    print("")
    print("EMPLOYEE 4")
    print("Username : employee04")
    print("Password : Employee@123")

    print("")
    print("==========================================")


if __name__ == "__main__":
    seed_data()
    