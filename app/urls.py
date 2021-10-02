from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.api_over_view, name="api_over_view"),
    path('api/v1/register/', views.register, name="register"),

    path('api/v1/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/v1/list/snippet/', views.snippet_list, name="snippet_list"),
    path('api/v1/detail/snippet/<int:id>/', views.snippet_detail, name="snippet_detail"),
    path('api/v1/create/snippet/', views.create_snippet, name="create_snippet"),
    path('api/v1/delete/snippet/<int:id>/', views.delete_snippet, name="delete_snippet"),
    path('api/v1/update/snippet/<int:id>/', views.update_snippet, name="update_snippet"),

    path('api/v1/list/tag/', views.tag_list, name="tag_list"),
    path('api/v1/detail/tag/<int:id>/', views.tag_detail, name="tag_detail"),
]
