from django.urls import path
from .views import ReviewViewSet, reviews_page

review_list = ReviewViewSet.as_view({
    "get": "list",
    "post": "create",
})

review_detail = ReviewViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

urlpatterns = [
    # HTML страница
    path("", reviews_page, name="reviews_page"),

    # JSON API
    path("data/", review_list, name="reviews_api_list"),
    path("data/<int:pk>/", review_detail, name="reviews_api_detail"),
]