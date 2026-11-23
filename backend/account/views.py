from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils import timezone
from django.db import transaction
from django.db.models import Max

from .models import Asset, User , ServiceCall
from .serializers import AssetSerializer, UserSerializer, LoginTokenSerializers , ServiceCallSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenSerializers


class AssetRolePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return user.role in ["ADMIN", "TECHNICIAN", "EMPLOYEE"]

        return user.role == "ADMIN"


class IsAdminRole(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return user.is_authenticated and user.role == "ADMIN"


class AssetViewSet(ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated, AssetRolePermission]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Asset.objects.all()

        elif user.role == "EMPLOYEE":
            return Asset.objects.filter(current_custodian=user)

        elif user.role == "TECHNICIAN":
            return Asset.objects.all()

        return Asset.objects.none()

    def perform_update(self, serializer):
        custodian = serializer.validated_data.get("current_custodian")

        if custodian:
            serializer.save(current_department=custodian.department, status=Asset.Status.ASSIGNED)
        else:
            serializer.save()


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    
class ServiceCallPermission(BasePermission):
        
    def has_permission(self,request,view):
        user = request.user
        
        if not user or not user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS :
            return user.role in ["ADMIN","EMPLOYEE","TECHNICIAN"]
        
        if request.method == "POST":
            return user.role in ["ADMIN","EMPLOYEE"]
        return user.role in ["ADMIN","TECHNICIAN"]
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == "ADMIN":
            return True
        
        if request.method in SAFE_METHODS:
            if user.role == "EMPLOYEE":
                return obj.reported_by_id == user.id
            if user.role == "TECHNICIAN":
                return obj.assigned_technician_id == user.id
        if user.role == "TECHNICIAN":
            return obj.assigned_technician_id == user.id
        
        return False
    
class ServiceCallViewSet(ModelViewSet):
    serializer_class = ServiceCallSerializer 
    permission_classes = [IsAuthenticated , ServiceCallPermission]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == "ADMIN":
            return ServiceCall.objects.all().order_by("-created_at")
        elif user.role == "TECHNICIAN" :
            return ServiceCall.objects.filter(assigned_technician=user).order_by("-created_at")
        elif user.role == "EMPLOYEE":
            return ServiceCall.objects.filter(reported_by=user).order_by("-created_at")
        return ServiceCall.objects.none()
    
    def perform_create(self, serializer):
        year = timezone.now().year

        with transaction.atomic():
            last_call = (
                ServiceCall.objects
                .select_for_update()
                .filter(ticket_id__startswith=f"CALL-{year}-")
                .order_by("-id")
                .first()
            )

            if last_call:
                last_number = int(last_call.ticket_id.split("-")[-1])
                next_number = last_number + 1
            else:
                next_number = 1

            ticket_id = f"CALL-{year}-{next_number:04d}"

            serializer.save(
                ticket_id=ticket_id,
                reported_by=self.request.user
            )
    @action(detail=False, methods=["get"], url_path="my-tickets")
    def my_tickets(self,request):
        tickets = ServiceCall.objects.filter(reported_by=request.user).order_by("-create_at")
        serializer = self.get_serializer(tickets,many=True)
        
        return Response(serializer.data , status=HTTP_200_OK)