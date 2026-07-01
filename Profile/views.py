from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, BorrowRequest
from .forms import Profile_Form
from hr.models import Product, BorrowRequest as HRBorrowRequest
from django.contrib.auth import login as auth_login, logout as auth_logout
from hr.models import Product


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        profile, created = Profile.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            defaults={
                'dob': request.POST.get('dob') or None,
                'phone_number': request.POST.get('phone_number'),
                'email': request.POST.get('email'),
                'role': request.POST.get('role'),
            },
        )
        if not created:
            profile.dob = request.POST.get('dob') or profile.dob
            profile.phone_number = request.POST.get('phone_number')
            profile.email = request.POST.get('email') or profile.email
            profile.role = request.POST.get('role')
            profile.save()

        request.session.flush()
        request.session['profile_id'] = profile.id   # <-- THIS is "which id I registered as"
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('staff')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.flush()
    auth_logout(request)
    return redirect('register')


def staff(request):
    profile_id = request.session.get('profile_id')                      # read the id
    current_profile = Profile.objects.filter(id=profile_id).first() if profile_id else None

    if request.method == 'POST' and 'borrow_product' in request.POST:
        if not current_profile:
            return redirect('register')
        product_id = request.POST.get('product_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        take_time = request.POST.get('take_time')
        bring_time = request.POST.get('bring_time')
        if product_id and first_name and take_time and bring_time:
            HRBorrowRequest.objects.create(
                product_id=product_id,
                requested_by=current_profile,      # <-- stamp the request with that id
                first_name=first_name,
                last_name=last_name,
                take_time=take_time,
                bring_time=bring_time,
            )
        return redirect('staff')

    if current_profile:
        profiles = Profile.objects.filter(id=current_profile.id)
        borrow_requests = HRBorrowRequest.objects.filter(
            requested_by=current_profile               # <-- only pull rows stamped with that id
        ).select_related('product').order_by('-submitted_at')
    else:
        profiles = Profile.objects.none()
        borrow_requests = HRBorrowRequest.objects.none()

    products = Product.objects.all()
    return render(request, 'staff.html', {
        'profiles': profiles, 'products': products, 'borrow_requests': borrow_requests,
    })


def delete_profile(request, id):
    profile = get_object_or_404(Profile, id=id)
    profile.delete()
    return redirect('staff')


def update(request, id):
    instance = get_object_or_404(Profile, id=id)
    if request.method == "POST":
        form = Profile_Form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('staff')
    else:
        form = Profile_Form(instance=instance)
    return render(request, 'register.html', {'form': form, 'is_update': True})

def delete_history_request(request, id):
    profile_id = request.session.get('profile_id')
    req = get_object_or_404(HRBorrowRequest, id=id, requested_by_id=profile_id)
    if request.method == "POST":
        req.delete()
    return redirect('staff')

def delete_request_product(request, id):
    """Lets staff delete a product from their Request tab; redirects back to staff page."""
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
    return redirect('staff')