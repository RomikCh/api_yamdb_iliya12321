from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet,
    UserViewSet,
    APIUserMe,
    APISignUp
)

router_v1 = DefaultRouter()

router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<rewiew_id>\d+/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/users/me/', APIUserMe.as_view()),
    path('v1/auth/signup/', APISignUp.as_view()),
    path('v1/', include(router_v1.urls)),
]
