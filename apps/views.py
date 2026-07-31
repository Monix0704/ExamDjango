from django.contrib.auth import login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, CreateView

from apps.models import User, Post


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return redirect('register')
        if User.objects.filter(first_name=first_name).exists():
            return redirect("register")
        hashed_password = make_password(password)
        User.objects.create_user(username=username, password=hashed_password)
        return render(request, 'login.html', {"position": "login"})
    else:
        return render(request, 'register.html', {"position": "register"})

class DashboardTemplateView(TemplateView):
    template_name = 'dashboard.html'
def login_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        session_user = User.objects.filter(first_name=first_name).first()
        if session_user:
            if check_password(password, session_user.password):
                login(request, session_user)
                return redirect('dashboard')
        return redirect('login')
    else:
        return render(request, 'login.html', {"position": "login"})

class IndexTemplateView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['page'] = self.request.GET.get("page")
        return data

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    pass

