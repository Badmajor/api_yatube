from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()
subrouter = DefaultRouter()

router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
subrouter.register(r'comments', CommentViewSet)


urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
    path('v1/posts/<int:post_id>/', include(subrouter.urls)),
]
