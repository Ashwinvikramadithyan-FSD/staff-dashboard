from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Profile
from .forms import RegisterForm

# NOTE: If you moved your models, update the line below:
# from .models import Profile, Product, HRBorrowRequest

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    error = None
    submitted_username = ''
    if request.method == "POST":
        submitted_username = request.POST.get('username', '').strip()
        submitted_password = request.POST.get('password', '')
        profile = Profile.objects.filter(username=submitted_username).first()

        if profile is None or not check_password(submitted_password, profile.password):
            error = 'Invalid username or password.'
        else:
            request.session.flush()
            request.session['profile_id'] = profile.id
            # Redirecting all users to staff since 'hr_dashboard' was removed
            return redirect('staff')

    return render(request, 'login.html', {'error': error, 'username': submitted_username})


def logout(request):
    request.session.flush()
    return redirect('login')


def staff(request):
    profile_id = request.session.get('profile_id')
    current_profile = Profile.objects.filter(id=profile_id).first() if profile_id else None
    
    # NOTE: Functionality below is commented out because it depends on 
    # models from the 'hr' app which you are deleting.
    borrow_error = None
    reopen_product = None
    borrow_requests = None
    products = None

    if request.method == 'POST' and 'borrow_product' in request.POST:
        borrow_error = "Borrowing functionality is currently disabled."

    if current_profile:
        profiles = Profile.objects.filter(id=current_profile.id)
    else:
        profiles = Profile.objects.none()

    return render(request, 'staff.html', {
        'profiles': profiles, 
        'products': products, 
        'borrow_requests': borrow_requests,
        'borrow_error': borrow_error, 
        'reopen_product': reopen_product,
    })


def delete_history_request(request, id):
    # This will fail unless HRBorrowRequest is moved to Profile/models.py
    # req = get_object_or_404(HRBorrowRequest, id=id, requested_by_id=request.session.get('profile_id'))
    # if request.method == "POST":
    #     req.delete()
    return redirect('staff')


def delete_request_product(request, id):
    # This will fail unless Product is moved to Profile/models.py
    # product = get_object_or_404(Product, id=id)
    # if request.method == "POST":
    #     product.delete()
    return redirect('staff')