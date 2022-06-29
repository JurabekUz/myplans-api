from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from plans.views import PlanViewSet, HabitViewSet

router = DefaultRouter()
router.register('plans', PlanViewSet, 'plans')
router.register('habits', HabitViewSet, 'habits')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-auth-token/', views.obtain_auth_token),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/signup/', include('dj_rest_auth.registration.urls')),
    path('', include(router.urls)),
]
