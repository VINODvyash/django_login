from django.urls import path

#from .views import health,login_view,profile,register,admin_dashboard, logout_view, protected_api, update_profile, change_password, forgot_password, reset_password

from .views import (
    health, login_view, profile, register,
    admin_dashboard, logout_view, protected_api,
    update_profile, change_password,
    forgot_password, reset_password,
    MeAPIView,TaskViewSet

)
from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')


urlpatterns = [
    #path('api/', include('accounts.urls')),

    path('health/', health),       # correct API
    path('login/', login_view, name='login'),    # correct API
    path('profile/', profile),     # correct API
    path('register/',register),    # correct API
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'), # JWT Token Refresh API correct API
    path('admin/dashboard/', admin_dashboard),  # Admin only view
    path('logout/', logout_view), # correct API
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), #correct API
    path('protected/', protected_api), #correct
    path('update-profile/', update_profile,name='update-profile'), #compllicated
    path('change-password/', change_password), #corect API
    path('forgot-password/', forgot_password), #WORKING 
    path('reset-password/', reset_password), #working
    path('me/', MeAPIView.as_view(), name='me'), #Working
    #path('tasks/',TaskAPIView.as_view(), name="tasks"),

]

urlpatterns += router.urls

# from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet

# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet, basename='tasks')

# urlpatterns = router.urls