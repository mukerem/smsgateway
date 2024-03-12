from django.core.exceptions import PermissionDenied
from account.models import User
from django.utils import timezone
from django.shortcuts import redirect

def admin_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_auth_and_user_exist(function):
    def wrap(request, *args, **kwargs):
        try:
            User.objects.get(pk=kwargs['user_id'])
        except User.DoesNotExist:
            raise PermissionDenied
        if request.user.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# staff user decorator
def staff_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'staff':
            return function(request, *args, **kwargs)
        else:
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# guest user decorator

def guest_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'guest':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def guest_auth_and_user_exist(function):
    def wrap(request, *args, **kwargs):
        try:
            User.objects.get(pk=kwargs['user_id'])
        except User.DoesNotExist:
            # raise PermissionDenied
            return redirect('homepage')
        if request.user.role == 'guest':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_or_guest_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'admin' or request.user.role == 'guest':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_or_staff_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'admin' or request.user.role == 'staff':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def admin_staff_guest_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'admin' or \
            request.user.role == 'staff' or request.user.role == 'guest':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



def staff_or_guest_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'staff' or request.user.role == 'guest':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def staff_auth_and_user_exist(function):
    def wrap(request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['user_id'])
            if user.campus != request.user.campus:
                return redirect('homepage')
        except User.DoesNotExist:
            return redirect('homepage')
        if request.user.role == 'staff':
            return function(request, *args, **kwargs)
        else:
            # raise PermissionDenied
            return redirect('homepage')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap