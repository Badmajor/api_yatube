from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import PostViewSet, GroupViewSet, CommentView

router = DefaultRouter()

router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/<int:pk>/',
         CommentView.as_view(
             {
                 'get': 'retrieve',
                 'delete': 'destroy',
                 'put': 'update',
                 'patch': 'update'
             },
         )
         )]
