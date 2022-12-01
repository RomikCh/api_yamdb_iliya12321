from django.urls import include, path
from rest_framework.routers import DefaultRouter


from api.views import (
    CommentViewSet, TitleViewSet, CategoryViewSet, GenreViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet)
router_v1.register(r'^titles/(?P<title_id>\d+)/reviews/', TitleViewSet, basename='titles')
router_v1.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<rewiew_id>\d+/comments', CommentViewSet, basename='comments')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
