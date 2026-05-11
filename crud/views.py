from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Gender, User
from .forms import GenderForm, UserForm, UserEditForm
import hashlib


def hash_pw(raw):
    return hashlib.sha256(raw.encode()).hexdigest()


# ───────────────────────────────────────────────────── genders ─────────────────────────────────────────────────────

def GendersList(request):
    genders = Gender.objects.all().order_by('gender_id')
    return render(request, 'gender/GendersList.html', {'genders': genders})


def AddGender(request):
    form = GenderForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Gender added successfully.')
        return redirect('GendersList')
    return render(request, 'gender/AddGender.html', {'form': form})


def EditGender(request, pk):
    gender = get_object_or_404(Gender, gender_id=pk)
    form = GenderForm(request.POST or None, instance=gender)
    if form.is_valid():
        form.save()
        messages.success(request, 'Gender updated successfully.')
        return redirect('GendersList')
    return render(request, 'gender/EditGender.html', {
        'form': form, 'gender': gender
    })


def DeleteGender(request, pk):
    gender = get_object_or_404(Gender, gender_id=pk)
    if request.method == 'POST':
        gender.delete()
        messages.success(request, 'Gender deleted.')
        return redirect('GendersList')
    return render(request, 'gender/DeleteGender.html', {'gender': gender})


# ─────────────────────────────────────────────────────── users ───────────────────────────────────────────────────────

def UsersList(request):
    query = request.GET.get('q', '')
    qs = User.objects.select_related('gender').order_by('user_id')
    if query:
        qs = qs.filter(email__icontains=query)
    paginator = Paginator(qs, 5)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    return render(request, 'user/UsersList.html', {
        'users': users, 'query': query
    })

def AddUser(request):
    form = UserForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.password = hash_pw(form.cleaned_data['password'])
        user.save()
        messages.success(request, 'User added successfully.')
        
        return redirect('UsersList')
    return render(request, 'user/AddUser.html', {'form': form})


def EditUser(request, pk):
    user = get_object_or_404(User, user_id=pk)
    form = UserEditForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        updated = form.save(commit=False)
        pw = form.cleaned_data.get('password')
        if pw:
            updated.password = hash_pw(pw)
        updated.save()
        messages.success(request, 'User updated successfully.')
        
        return redirect('UsersList')
    return render(request, 'user/EditUser.html', {'form': form, 'user': user})


def DeleteUser(request, pk):
    user = get_object_or_404(User, user_id=pk)
    if request.method == 'POST':
        if user.profile_pic:
            user.profile_pic.delete(save=False)
        user.delete()
        messages.success(request, 'User deleted.')
        
        return redirect('UsersList')
    return render(request, 'user/DeleteUser.html', {'user': user})