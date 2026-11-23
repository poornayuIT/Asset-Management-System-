from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import(
    Department,
    User,
    Asset,
    ServiceCall,
    WorkLog,
)

user = get_user_model()

#serializers

class LoginTokenSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["role"] = user.role
        return token
    
    def validate(self, attrs):
        data=super().validate(attrs)
        data["username"] = self.user.username
        data["role"] = self.user.role
        
        return data
    

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields = ["id","name"]
        
class UserSerializer(serializers.ModelSerializer):
    department_name= serializers.CharField(source="department.name",read_only=True)
    class Meta:
        model=User
        fields = ["id","username","first_name","last_name","email","mobile","role","department","department_name"]
        read_only_fields=["id","deapartment_name"]
    
class AssetSerializer(serializers.ModelSerializer):
    current_department_name=serializers.CharField(source="current_department.name",read_only=True)
    current_custodian_name = serializers.CharField(source="current_custodian.username",read_only=True)
    
    class Meta:
        model=Asset
        fields=["id","asset_tag","asset_type","brand","model","serial_number","ram","storage","ip_address","mac_address","purchase_date","warranty_expiry","status","current_department","current_department_name","current_custodian","current_custodian_name","room_no",]
        
        read_only_fields=["id","current_department_name","current_custodian_name","status",]

class ServiceCallSerializer(serializers.ModelSerializer):
    asset_tag=serializers.CharField(source="asset.asset_tag",read_only=True)
    reported_by = serializers.PrimaryKeyRelatedField(read_only=True)

    reported_by_name = serializers.CharField(source="reported_by.username",read_only=True)
    assigned_technician_name=serializers.CharField(source="assigned_technician.username",read_only=True)
    
    class Meta:
        model=ServiceCall
        fields=["id","ticket_id","asset","asset_tag","reported_by","reported_by_name","assigned_technician","assigned_technician_name","category","description","severity","status","employee_verified","verified_at","created_at","updated_at"]
        read_only_fields=["id","ticket_id","asset_tag","reported_by_name","assigned_technician_name","verified_at","created_at","updated_at"]


class WorkLogSerializer(serializers.ModelSerializer):
    ticket_id=serializers.CharField(source="service_call.ticket_id",read_only=True)
    technician_name=serializers.CharField(source="technician.username",read_only=True)
    
    class Meta:
        model=WorkLog
        fields=["id","service_call","ticket_id","technician","technician_name","description","created_at"]
        read_only_fields=["id","ticket_id","technician_name","created_at"]
        
class AssetAssignmentSerializer(serializers.Serializer):
    employee_id=serializers.IntegerField()
    department_id=serializers.IntegerField()
    room_no=serializers.CharField(max_length=15,required=False,allow_blank=True)
    
    
    
    