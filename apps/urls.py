from django.urls import path

from apps.views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),

    path('login/', LoginFormView.as_view(), name='login'),

    path('register/', RegisterFormView.as_view(), name='register'),

    path('create-post/', PostCreateView.as_view(), name='create-post'),

    path('logout/', logout_view, name='logout'),

    path('delete-post/<int:id>', PostDeleteView.as_view(), name='delete-post'),

    path('post-detail/<int:id>', PostDetailView.as_view(), name='post-detail'),

    path('create-comment/<int:post_id>', CommentCreateView.as_view(), name='create-comment')
]
