from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('groups', views.GroupViewSet)
comment_router = SimpleRouter()
comment_router.register(
    'comments',
    views.CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/posts/<int:post_id>/', include(comment_router.urls)),
    path('v1/follow/', views.FollowViewSet.as_view()),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
