from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AvailabilityViewSet, EmployeProjectViewSet, EmployeeViewSet, KPIDashboardView, NotificationViewSet, ProjectViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')  
router.register(r'projects', ProjectViewSet, basename='project')  
router.register(r'employeproject', EmployeProjectViewSet, basename='employeproject')
router.register(r'availiblity', AvailabilityViewSet, basename='availability')  
router.register(r'notification', NotificationViewSet, basename='notification')


urlpatterns = router.urls
urlpatterns += [
    path('kpi/', KPIDashboardView.as_view(), name='kpi'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)