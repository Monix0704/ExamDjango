from django.urls import path
from django.views import View

from apps.views import register_view, login_view, IndexTemplateView, DashboardTemplateView, PostDetailView, PostCreateView

urlpatterns = [
    path("auth/login", login_view, name="login"),
    path("auth/register", register_view, name="register"),
    path('', IndexTemplateView.as_view(), name="dashboard"),
    path("dashboard", DashboardTemplateView.as_view(), name="dashboard"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create', PostCreateView.as_view(), name='post_create'),

]