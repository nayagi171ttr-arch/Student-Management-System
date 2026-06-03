from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # Captures standard canonical UUID patterns inside the URL address path bar
    path('admin-panel/<uuid:user_uuid>/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/<uuid:user_uuid>/create/', views.create_user_action, name='create_user_action'),
    
    path('staff-panel/<uuid:user_uuid>/', views.staff_dashboard, name='staff_dashboard'),
    path('student-panel/<uuid:user_uuid>/', views.student_dashboard, name='student_dashboard'),
]