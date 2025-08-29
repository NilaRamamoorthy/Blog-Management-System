from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),  # FBV homepage
    path("posts/", views.PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/new/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
]
