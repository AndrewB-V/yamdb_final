from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import (AdminViewSet, APITokenCreate, APIUserCreate,
                    CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = SimpleRouter()

app_name = 'api'

router_v1.register(
    'users',
    AdminViewSet
)

router_v1.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

VERSION_PARAM = 'api/v1'

auth_patterns = [
    path('signup/', APIUserCreate.as_view()),
    path('token/', APITokenCreate.as_view()),
]

urlpatterns = [
    path(f'{VERSION_PARAM}/', include(router_v1.urls)),
    path(f'{VERSION_PARAM}/auth/', include(auth_patterns)),
]
