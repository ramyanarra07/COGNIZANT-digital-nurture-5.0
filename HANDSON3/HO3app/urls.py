from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

task1_patterns = [
    path('courses-basic/', views.CourseListView.as_view()),
    path('courses-basic/<int:pk>/', views.CourseDetailView.as_view()),
]

router = DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('students', views.StudentViewSet)
router.register('enrollments', views.EnrollmentViewSet)

urlpatterns = task1_patterns + router.urls