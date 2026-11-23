from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AssetViewSet,UsersViewSet,LoginView,ServiceCallViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router=DefaultRouter()
router.register("assets",AssetViewSet,basename="assets")
router.register("users",UsersViewSet,basename="users")
router.register(r"service-calls",ServiceCallViewSet,basename="service-call")


urlpatterns=[
    path("",include(router.urls)),
    path("token/",LoginView.as_view(),name="token_obtain_pair"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
]