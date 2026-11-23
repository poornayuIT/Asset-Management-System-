from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):

    class Role(models.TextChoices):
        EMPLOYEE = "EMPLOYEE"
        TECHNICIAN = "TECHNICIAN" 
        ADMIN = "ADMIN" 

    mobile = models.CharField(max_length=15,unique=True)
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.EMPLOYEE)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True,related_name="users")

    def __str__(self):
        return self.username

class Asset(models.Model):

    class AssetType(models.TextChoices):
        DESKTOP = "DESKTOP"
        LAPTOP = "LAPTOP"
        NETWORK_PRINTER = "NETWORK_PRINTER" 
        SCANNER = "SCANNER"

    class Status(models.TextChoices):
        IN_STOCK = "IN_STOCK"
        ASSIGNED = "ASSIGNED"
        UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
        SCRAPPED = "SCRAPPED"

    asset_tag = models.CharField(max_length=50,unique=True)
    asset_type = models.CharField(max_length=30,choices=AssetType.choices)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100,unique=True)
    ram = models.CharField(max_length=50,blank=True)
    storage = models.CharField(max_length=50,blank=True)
    ip_address = models.GenericIPAddressField(null=True,blank=True)
    mac_address = models.CharField(max_length=50,blank=True)
    purchase_date = models.DateField(null=True,blank=True)
    warranty_expiry = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=30,choices=Status.choices,default=Status.IN_STOCK)
    current_department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True,related_name="assets")
    current_custodian = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="assigned_assets")
    room_no=models.CharField(max_length=10,blank=True)

    def __str__(self):
        return self.asset_tag

# SERVICE CALL
class ServiceCall(models.Model):

    class Category(models.TextChoices):
        HARDWARE_FAILURE = "HARDWARE_FAILURE"
        SOFTWARE_CRASH = "SOFTWARE_CRASH"
        NETWORK = "NETWORK"
        CONSUMABLES = "CONSUMABLES"

    class Severity(models.TextChoices):
        LOW = "LOW"
        MEDIUM = "MEDIUM"
        HIGH = "HIGH"
        CRITICAL = "CRITICAL"

    class Status(models.TextChoices):
        LOGGED = "LOGGED"
        ASSIGNED = "ASSIGNED"
        IN_PROGRESS = "IN_PROGRESS"
        RESOLVED = "RESOLVED"
        CLOSED = "CLOSED"

    ticket_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="service_calls"
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reported_service_calls"
    )

    assigned_technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_service_calls"
    )

    category = models.CharField(
        max_length=30,
        choices=Category.choices
    )

    description = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=Severity.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.LOGGED
    )

    employee_verified = models.BooleanField(default=False)

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)    
#worklog database
class WorkLog(models.Model):

    service_call = models.ForeignKey(ServiceCall,on_delete=models.CASCADE,related_name="work_logs")
    technician = models.ForeignKey(User,on_delete=models.PROTECT,related_name="work_logs")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Work log for {self.service_call.ticket_id}"