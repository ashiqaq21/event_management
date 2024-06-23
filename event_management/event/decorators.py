from django.http import HttpResponse
from rest_framework import status
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def login_required_view(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapped

def organizer_required(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'organizer':
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapped

def admin_required(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapped
