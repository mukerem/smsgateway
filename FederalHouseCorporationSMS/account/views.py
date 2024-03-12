from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.decorators import admin_auth, admin_auth_and_user_exist
from account.models import User
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db import IntegrityError
from account.validators import email_validate
import csv
from account.forms import EditMyProfile, EditUserProfile, AddUser,\
    CSVUserUpload, ChangePassword
from django.contrib.auth.forms import AuthenticationForm
from .pagination import page_number_pagination

# Create your views here.
def index(request):
    print(12)
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        return render(request, 'registration/login.html', {'form': form})


def check_base_site(request):
    if request.user.role == 'admin':
        base = 'admin_base_site.html'
    elif request.user.role == 'staff':
        base = 'staff_base_site.html'
    elif request.user.role == 'guest':
        base = 'guest_base_site.html'
    return base


@login_required
def homepage(request):
    if request.user.role == 'super admin':
        return redirect('/admin/')
    elif request.user.role == 'admin':
        return render(request, 'admin_index.html')
    elif request.user.role == 'staff':
        return render(request, 'staff_index.html')
    elif request.user.role == 'guest':
        return render(request, 'guest_index.html')


@login_required
def profile(request):
    if request.method == "POST":
        form = EditMyProfile(request.POST, instance=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "successfully update.")
            return redirect('profile')
    else:
        form = EditMyProfile(instance=request.user)

    base = check_base_site(request)
    return render(request, 'profile.html', {'form': form, 'base_site': base})


@login_required
def change_password(request):
    if request.method == "POST":

        form = ChangePassword(request.POST, password=request.user.password)
        if form.is_valid():
            new_password = request.POST.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "The password was changed successfully.")
    else:
        form = ChangePassword(password=request.user.password)

    base = check_base_site(request)
    return render(request, 'change_password.html', {'form': form,  'base_site': base})


@login_required
@admin_auth
def user_list(request):

    staff_user = User.objects.filter(
        role="staff").order_by('first_name', 'last_name')
    admin_user = User.objects.filter(
        role="admin").order_by('first_name', 'last_name')
    guest_user = User.objects.filter(
        role="guest").order_by('first_name', 'last_name')
    
    page_number = request.GET.get('page', 1)
    role = request.GET.get('role', "staff")
    staff_page_number = 1
    guest_page_number = 1
    admin_page_number = 1

    if role == 'staff': staff_page_number=page_number
    elif role == 'guest': guest_page_number=page_number
    elif role == 'admin': admin_page_number=page_number
    
    staff_user, staff_paginator = page_number_pagination(request, staff_user, staff_page_number)
    guest_user, guest_paginator = page_number_pagination(request, guest_user, guest_page_number)
    admin_user, admin_paginator = page_number_pagination(request, admin_user, admin_page_number)

    context = {
        'staff_user': staff_user,
        'admin_user': admin_user,
        'guest_user': guest_user,
        'staff_paginator': staff_paginator,
        'admin_paginator': admin_paginator,
        'guest_paginator': guest_paginator,
        "role": role,
    }
    return render(request, 'user_list.html', context)


@login_required
@admin_auth_and_user_exist
def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'delete_user.html', {'this_user': user, 'user': 'hover'})


@login_required
@admin_auth_and_user_exist
def delete_user_done(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.role == "admin":
        messages.error(request, "It is not allowed to delete admin user.")
        return redirect('user')
    user.delete()
    messages.success(request, "user " + user.name +
                     " was deleted successfully.")
    return redirect('user')


@login_required
@admin_auth_and_user_exist
def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        form = EditUserProfile(request.POST, instance=user)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "The user " +
                             user.first_name+" was update successfully.")
            return redirect('user')
    else:
        form = EditUserProfile(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'user_id': user.id})


@login_required
@admin_auth
def user_register(request):
    if request.method == "POST":
        form = AddUser(request.POST)
        if form.is_valid():
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789@#$%&*'
            secret_key = get_random_string(8, chars)
            post = form.save(commit=False)
            post.set_password(secret_key)
            post.save()
            messages.success(request, "user "+post.name +
                             " was added successfully.")
            return redirect('user_register')
    else:
        form = AddUser()
    form1 = CSVUserUpload()
    return render(request, 'user_register.html', {'form': form, 'form1': form1})


def validate_data(request, first_name, last_name, email, line_number):
    if not first_name:
        messages.error(request, "invalid first_name in line " + str(line_number))
        return 0

    if not last_name:
        messages.error(request, "invalid last_name for user " + first_name)
        return 0

    if not email_validate(email):
        messages.error(request, "invalid email for user " + first_name)
        return 0
    else:
        try:
            User.objects.get(email=email)
            messages.error(request, "email " +
                           email + " was already exists.")
            return 0
        except User.DoesNotExist:
            pass

    return 1


def register_csv(request, csv_file):
    if not (csv_file.content_type == 'text/csv' or csv_file.content_type == 'application/vnd.ms-excel'):
        messages.error(request, "The file is not csv format.")
        return redirect('user_register_csv')
    else:
        decoded_file = csv_file.read().decode('utf-7').splitlines()
        reader = csv.DictReader(decoded_file)
        line_number = 0
        for row in reader:
            # basic info
            try:
                first_name = row['first_name'].strip()
                last_name = row['last_name'].strip()
                email = row['email'].strip()
                role = row['role'].strip()
            except KeyError:
                messages.error(request, "invalid column header in csv file.Column headers must be contain first_name,"
                               " last_name, email and role.")
                return redirect('user_register_csv')

            # validate data
            val = validate_data(request, first_name, last_name, email, line_number)

            if val == 0:
                continue

            # role info
            if role not in ["admin", "staff", "guest"]:
                messages.error(request, "invalid role for user " + first_name)
                continue

            try:
                chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
                if 'password' in row:
                    secret_key = row['password']
                else:
                    secret_key = get_random_string(8, chars)
                obj, created = User.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    role=role,
                )
                obj.set_password(secret_key)
                obj.save()

            except IntegrityError:
                messages.error(
                    request, "invalid information for user " + first_name)
            line_number += 1
    if not line_number:
        messages.error(request, " no user register.")
    else:
        messages.success(request, str(line_number) +
                         " user register successfully.")
    return redirect('user_register_csv')


@login_required
@admin_auth
def user_register_csv(request):
    if request.method == "POST":
        form1 = CSVUserUpload(request.POST, request.FILES)
        if form1.is_valid():
            file = request.FILES.get('file')
            register_csv(request, file)
            return redirect('user_register')
    else:
        form1 = CSVUserUpload()
    form = AddUser()
    return render(request, 'user_register.html', {'form': form, 'form1': form1, 'user': 'hover'})